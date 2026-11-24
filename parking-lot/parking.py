from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod
import math

class VehicleType(Enum):
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    TRUCK = "truck"

class SpotSize(Enum):
    MOTORCYCLE_SPOT = "motorcycle_spot"
    COMPACT_SPOT = "compact_spot"
    LARGE_SPOT = "large_spot"

class SpotStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"


class TicketStatus(Enum):
    ACTIVE="active"
    CLOSED="closed"

FIT_MAP = {
            VehicleType.TRUCK : [SpotSize.LARGE_SPOT],
            VehicleType.CAR: [SpotSize.LARGE_SPOT,SpotSize.COMPACT_SPOT] ,
            VehicleType.MOTORCYCLE: [SpotSize.LARGE_SPOT,SpotSize.COMPACT_SPOT,SpotSize.MOTORCYCLE_SPOT]
}

class Vehicle:
    def __init__(self,vehicle_type: VehicleType, registration_number: str):
        self.vehicle_type = vehicle_type
        self.registration_number = registration_number

    
class ParkingSpot:
    def __init__(self,spot_id:str,spot_size:SpotSize,floor_number: int):
        self.spot_id=spot_id
        self.spot_size=spot_size
        self.spot_status = SpotStatus.AVAILABLE
        self.floor_number = floor_number

    def can_fit(self,vehicle:Vehicle)->bool:
        return self.spot_size in FIT_MAP[vehicle.vehicle_type]

    def is_free(self)->bool:
        return self.spot_status == SpotStatus.AVAILABLE
    
    def occupy(self):
        if self.spot_status != SpotStatus.AVAILABLE:
            raise ValueError("Spot is already occupied")
        self.spot_status = SpotStatus.OCCUPIED

    def release(self):
        if self.spot_status == SpotStatus.AVAILABLE:
            raise ValueError("Spot is already free")
        self.spot_status = SpotStatus.AVAILABLE

class Floor:
    def __init__(self,floor_number:int, spots: list[ParkingSpot]):
        self.floor_number =floor_number
        self.spots = spots

class Ticket:
    def __init__(self,ticket_id: int,vehicle:Vehicle,parking_spot:ParkingSpot,entry_time:datetime):
        self.ticket_id=ticket_id
        self.entry_time=entry_time
        self.vehicle = vehicle
        self.parking_spot=parking_spot
        self.status = TicketStatus.ACTIVE
        self.exit_time = None

    def close(self,exit_time: datetime):
        if self.status == TicketStatus.CLOSED:
            raise ValueError("Ticket Already Closed")
        self.status = TicketStatus.CLOSED
        self.exit_time = exit_time

class AllocationStrategy(ABC):
    @abstractmethod
    def allocate(self, floors: list[Floor], vehicle: Vehicle) -> ParkingSpot | None:
        pass

class LowestFirst(AllocationStrategy):
    def allocate(self, floors, vehicle):
        sorted_floors = sorted(floors,key= lambda f: f.floor_number)
        for floor in sorted_floors:
            for spot in floor.spots:
                if spot.is_free() and spot.can_fit(vehicle):
                    return spot
        return None

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, vehicle_type: VehicleType, entry_time: datetime, exit_time:datetime) -> float:
        pass

def billable_hours(entry_time, exit_time):
        if exit_time < entry_time:
            raise ValueError("Exit time is before entry time")
        return (exit_time - entry_time).total_seconds() / 3600


class HourlyRates(PricingStrategy):
    RATES = {
        VehicleType.MOTORCYCLE: 0.5,
        VehicleType.CAR: 1,
        VehicleType.TRUCK: 1.5,
    }

    def calculate(self, vehicle_type, entry_time, exit_time):
        return round(billable_hours(entry_time, exit_time) * self.RATES[vehicle_type], 2)

class WeekendRates(PricingStrategy):
    RATES = {
        VehicleType.MOTORCYCLE: 1,
        VehicleType.CAR: 1.5,
        VehicleType.TRUCK: 2,
    }
    def calculate(self, vehicle_type, entry_time, exit_time):
        return round(billable_hours(entry_time, exit_time) * self.RATES[vehicle_type], 2)
        

class ParkingLot():
    def __init__(self,floors: list[Floor],allocation_strategy: AllocationStrategy, pricing_strategy: PricingStrategy):
        self.floors = floors
        self.lookup_by_ticket = {}
        self.lookup_by_vehicle = {}
        self.allocation_strategy=allocation_strategy
        self.next_ticket_id =1
        self.pricing_strategy = pricing_strategy

    def set_pricing_strategy(self,strategy: PricingStrategy):
        self.pricing_strategy = strategy

    def entry(self,vehicle:Vehicle,entry_time: datetime):
        
        if vehicle.registration_number in self.lookup_by_vehicle:
            raise ValueError(f"Vehicle {vehicle.registration_number} Already Inside cant enter again!!")
        
        spot_found = self.allocation_strategy.allocate(self.floors,vehicle)

        if spot_found:
            spot_found.occupy()
            self.next_ticket_id = self.next_ticket_id + 1
            ticket = Ticket(self.next_ticket_id,vehicle,spot_found,entry_time)
            self.lookup_by_ticket[ticket.ticket_id] = ticket
            self.lookup_by_vehicle[vehicle.registration_number] = ticket
            return ticket
        else:
            raise ValueError(f"All Spots Full. Cant allocate this {vehicle.vehicle_type.name} now")

    def exit(self, ticket_id: int, exit_time: datetime):
        ticket: Ticket = self.lookup_by_ticket.get(ticket_id,None)
        if ticket == None:
            raise ValueError(f"{ticket_id} doesnt exist")
        if exit_time < ticket.entry_time :
            raise ValueError(f"Exit time ({exit_time}) is before Entry time({ticket.entry_time}) which is invalid")
        total_price = self.pricing_strategy.calculate(ticket.vehicle.vehicle_type,entry_time=ticket.entry_time,exit_time=exit_time)
        ticket.close(exit_time=exit_time)
        ticket.parking_spot.release()
        ticket_removed: Ticket=self.lookup_by_ticket.pop(ticket_id)
        self.lookup_by_vehicle.pop(ticket_removed.vehicle.registration_number)
        return total_price






def at(h, m=0, day=0):
    return datetime(2026, 11, 22 + day, h, m)

if __name__ == "__main__":
    t0 = datetime(2026, 11, 22, 9, 0)

    def check(label, actual, expected):
        status = "PASS" if actual == expected else "FAIL"
        print(f"{status}  {label}  (got {actual!r}, expected {expected!r})")

    def blocked(label, fn):
        try:
            fn()
            print(f"FAIL  {label}  (no error raised)")
        except ValueError as e:
            print(f"PASS  {label}  -> {e}")

    def make_lot(spot_defs, strategy=None, pricing=None):
        floors = [
            Floor(n, [ParkingSpot(sid, size, n) for sid, size in spots])
            for n, spots in spot_defs.items()
        ]
        return ParkingLot(floors, strategy or LowestFirst(), pricing or HourlyRates())

    bike = Vehicle(VehicleType.MOTORCYCLE, "M-1")
    car = Vehicle(VehicleType.CAR, "C-1")
    truck = Vehicle(VehicleType.TRUCK, "T-1")

    print("\n--- 1. Fit rules (every vehicle x every spot size) ---")
    expected_fit = {
        (VehicleType.MOTORCYCLE, SpotSize.MOTORCYCLE_SPOT): True,
        (VehicleType.MOTORCYCLE, SpotSize.COMPACT_SPOT): True,
        (VehicleType.MOTORCYCLE, SpotSize.LARGE_SPOT): True,
        (VehicleType.CAR, SpotSize.MOTORCYCLE_SPOT): False,
        (VehicleType.CAR, SpotSize.COMPACT_SPOT): True,
        (VehicleType.CAR, SpotSize.LARGE_SPOT): True,
        (VehicleType.TRUCK, SpotSize.MOTORCYCLE_SPOT): False,
        (VehicleType.TRUCK, SpotSize.COMPACT_SPOT): False,
        (VehicleType.TRUCK, SpotSize.LARGE_SPOT): True,
    }
    for (vtype, size), want in expected_fit.items():
        v = Vehicle(vtype, "X")
        s = ParkingSpot("S", size, 1)
        check(f"{vtype.name} in {size.name}", s.can_fit(v), want)

    print("\n--- 2. Spot guards ---")
    s = ParkingSpot("1-C1", SpotSize.COMPACT_SPOT, 1)
    check("new spot is free", s.is_free(), True)
    s.occupy()
    check("after occupy, not free", s.is_free(), False)
    blocked("occupy an occupied spot", s.occupy)
    s.release()
    check("after release, free", s.is_free(), True)
    blocked("release a free spot", s.release)

    print("\n--- 3. Ticket close ---")
    spot = ParkingSpot("1-L1", SpotSize.LARGE_SPOT, 1)
    t = Ticket(1, truck, spot, t0)
    check("new ticket is ACTIVE", t.status, TicketStatus.ACTIVE)
    check("new ticket has no exit time", t.exit_time, None)
    t.close(datetime(2026, 11, 22, 12, 0))
    check("closed ticket status", t.status, TicketStatus.CLOSED)
    check("closed ticket exit time", t.exit_time, datetime(2026, 11, 22, 12, 0))
    blocked("close a closed ticket", lambda: t.close(datetime(2026, 11, 22, 13, 0)))

    print("\n--- 4. LowestFirst allocation ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT)], 2: [("2-L1", SpotSize.LARGE_SPOT)]})
    strat = LowestFirst()
    check("car gets floor 1 compact", strat.allocate(lot.floors, car).spot_id, "1-C1")
    check("truck skips floor 1, gets floor 2 large", strat.allocate(lot.floors, truck).spot_id, "2-L1")
    check("floors passed in reverse order still pick lowest",
          strat.allocate(list(reversed(lot.floors)), car).spot_id, "1-C1")
    for f in lot.floors:
        for sp in f.spots:
            sp.occupy()
    check("everything occupied -> None", strat.allocate(lot.floors, car), None)

    print("\n--- 5. Entry: motorcycle takes the only LARGE spot, truck then refused (test 1) ---")
    lot = make_lot({1: [("1-L1", SpotSize.LARGE_SPOT)]})
    tk = lot.entry(bike, t0)
    check("bike got the LARGE spot", tk.parking_spot.spot_id, "1-L1")
    check("spot is now occupied", tk.parking_spot.is_free(), False)
    blocked("truck refused, no spot left", lambda: lot.entry(truck, t0))

    print("\n--- 6. Entry: truck refused when only COMPACT is free (test 2) ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT)]})
    blocked("truck refused", lambda: lot.entry(truck, t0))
    check("no ticket issued (by ticket)", len(lot.lookup_by_ticket), 0)
    check("no ticket issued (by vehicle)", len(lot.lookup_by_vehicle), 0)
    check("compact spot untouched", lot.floors[0].spots[0].is_free(), True)

    print("\n--- 7. Entry: same vehicle twice (test 3) ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT), ("1-C2", SpotSize.COMPACT_SPOT)]})
    first = lot.entry(car, t0)
    blocked("car enters again while inside", lambda: lot.entry(car, t0))
    check("still one ticket by id", len(lot.lookup_by_ticket), 1)
    check("still one ticket by vehicle", len(lot.lookup_by_vehicle), 1)
    check("second spot not consumed by the failed entry", lot.floors[0].spots[1].is_free(), True)
    check("map by vehicle points at the same ticket",
          lot.lookup_by_vehicle["C-1"] is first, True)

    print("\n--- 8. Entry: two vehicles never share a spot, and ticket IDs are unique ---")
    lot = make_lot({1: [(f"1-C{i}", SpotSize.COMPACT_SPOT) for i in range(1, 21)]})
    tickets = [lot.entry(Vehicle(VehicleType.CAR, f"CAR-{i}"), t0) for i in range(20)]
    check("20 unique ticket IDs", len({tk.ticket_id for tk in tickets}), 20)
    check("20 unique spots", len({tk.parking_spot.spot_id for tk in tickets}), 20)
    blocked("21st car refused, lot full", lambda: lot.entry(Vehicle(VehicleType.CAR, "CAR-21"), t0))
    check("lot still holds 20 tickets", len(lot.lookup_by_ticket), 20)

    print("\n--- 9. Entry: failed entry changes nothing, next valid one still works ---")
    lot = make_lot({1: [("1-L1", SpotSize.LARGE_SPOT)], 2: [("2-C1", SpotSize.COMPACT_SPOT)]})
    lot.entry(truck, t0)
    blocked("second truck refused", lambda: lot.entry(Vehicle(VehicleType.TRUCK, "T-2"), t0))
    check("tickets after refusal", len(lot.lookup_by_ticket), 1)
    tk = lot.entry(car, t0)
    check("car still gets floor 2 compact", tk.parking_spot.spot_id, "2-C1")

    hourly = HourlyRates()

    
    check("car 3h exact", hourly.calculate(VehicleType.CAR, at(9), at(12)), 3)
    check("car 3h30 exact", hourly.calculate(VehicleType.CAR, at(9), at(12, 30)), 3.5)
    check("car 90 min", hourly.calculate(VehicleType.CAR, at(9), at(10, 30)), 1.5)
    check("car 25h (crosses a day)", hourly.calculate(VehicleType.CAR, at(9), at(10, day=1)), 25)
    check("truck 2h", hourly.calculate(VehicleType.TRUCK, at(9), at(11)), 3.0)
    check("bike 5h", hourly.calculate(VehicleType.MOTORCYCLE, at(7), at(12)), 2.5)
    blocked("exit before entry", lambda: hourly.calculate(VehicleType.CAR, at(12), at(9)))

    print("\n--- 11. WeekendRates ---")
    weekend = WeekendRates()
    check("car 3h weekend", weekend.calculate(VehicleType.CAR, at(9), at(12)), 4.5)
    check("car 3h30 weekend", weekend.calculate(VehicleType.CAR, at(9), at(12, 30)), 5.25)
    check("truck 2h weekend", weekend.calculate(VehicleType.TRUCK, at(9), at(11)), 4.0)
    check("bike 2h weekend", weekend.calculate(VehicleType.MOTORCYCLE, at(9), at(11)), 4.5)
    check("same stay, different strategy, different fee",
          hourly.calculate(VehicleType.CAR, at(9), at(12)) != weekend.calculate(VehicleType.CAR, at(9), at(12)),
          True)
    blocked("weekend: exit before entry", lambda: weekend.calculate(VehicleType.CAR, at(12), at(9)))

    print("\n--- 12. Exit: fee, spot freed, maps cleaned ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT)]})
    tk = lot.entry(Vehicle(VehicleType.CAR, "C-1"), at(9))
    spot = tk.parking_spot
    fee = lot.exit(tk.ticket_id, at(12))
    check("car 3h hourly fee", fee, 3)
    check("spot is free after exit", spot.is_free(), True)
    check("ticket map empty", len(lot.lookup_by_ticket), 0)
    check("vehicle map empty", len(lot.lookup_by_vehicle), 0)
    check("ticket is CLOSED", tk.status, TicketStatus.CLOSED)
    check("ticket exit time recorded", tk.exit_time, at(12))

    print("\n--- 13. Exit: the freed spot is reusable, and the same car can re-enter ---")
    lot = make_lot({1: [("1-L1", SpotSize.LARGE_SPOT)]})
    tk1 = lot.entry(Vehicle(VehicleType.TRUCK, "T-1"), at(9))
    blocked("lot is full before exit", lambda: lot.entry(Vehicle(VehicleType.TRUCK, "T-2"), at(9, 5)))
    lot.exit(tk1.ticket_id, at(10))
    tk2 = lot.entry(Vehicle(VehicleType.TRUCK, "T-2"), at(10, 5))
    check("next truck takes the freed spot", tk2.parking_spot.spot_id, "1-L1")
    lot.exit(tk2.ticket_id, at(11))
    tk3 = lot.entry(Vehicle(VehicleType.TRUCK, "T-1"), at(11, 5))
    check("T-1 can re-enter after exiting", tk3.parking_spot.spot_id, "1-L1")
    check("new ticket ID differs from the old one", tk3.ticket_id != tk1.ticket_id, True)

    print("\n--- 14. Exit: unknown ticket ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT)]})
    tk = lot.entry(Vehicle(VehicleType.CAR, "C-1"), at(9))
    blocked("ticket ID that never existed", lambda: lot.exit(9999, at(10)))
    check("nothing changed: ticket still stored", len(lot.lookup_by_ticket), 1)
    check("nothing changed: spot still occupied", tk.parking_spot.is_free(), False)
    check("nothing changed: ticket still ACTIVE", tk.status, TicketStatus.ACTIVE)

    print("\n--- 15. Exit: reused ticket must not touch the spot's new occupant ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT)]})
    old = lot.entry(Vehicle(VehicleType.CAR, "C-1"), at(9))
    lot.exit(old.ticket_id, at(10))
    new = lot.entry(Vehicle(VehicleType.CAR, "C-2"), at(10, 5))
    blocked("second exit with the old ticket", lambda: lot.exit(old.ticket_id, at(11)))
    check("C-2 still holds the spot", new.parking_spot.is_free(), False)
    check("C-2 ticket still ACTIVE", new.status, TicketStatus.ACTIVE)
    check("C-2 still registered inside", "C-2" in lot.lookup_by_vehicle, True)

    print("\n--- 16. Exit: bad exit time leaves everything untouched, retry works ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT)]})
    tk = lot.entry(Vehicle(VehicleType.CAR, "C-1"), at(9))
    blocked("exit time before entry time", lambda: lot.exit(tk.ticket_id, at(8)))
    check("ticket still ACTIVE", tk.status, TicketStatus.ACTIVE)
    check("spot still occupied", tk.parking_spot.is_free(), False)
    check("still in ticket map", tk.ticket_id in lot.lookup_by_ticket, True)
    check("still in vehicle map", "C-1" in lot.lookup_by_vehicle, True)
    check("valid exit afterwards still works", lot.exit(tk.ticket_id, at(11)), 2)

    print("\n--- 17. Exit: two vehicles inside, one leaves ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT), ("1-L1", SpotSize.LARGE_SPOT)]})
    car_tk = lot.entry(Vehicle(VehicleType.CAR, "C-1"), at(9))
    truck_tk = lot.entry(Vehicle(VehicleType.TRUCK, "T-1"), at(9))
    check("truck 2h hourly fee", lot.exit(truck_tk.ticket_id, at(11)), 3.0)
    check("car still inside", car_tk.status, TicketStatus.ACTIVE)
    check("car spot still occupied", car_tk.parking_spot.is_free(), False)
    check("one ticket left", len(lot.lookup_by_ticket), 1)
    check("only C-1 registered", list(lot.lookup_by_vehicle.keys()), ["C-1"])

    print("\n--- 18. Swapping pricing strategy before exit (test 7) ---")
    lot = make_lot({1: [("1-C1", SpotSize.COMPACT_SPOT), ("1-C2", SpotSize.COMPACT_SPOT)]})
    tk_a = lot.entry(Vehicle(VehicleType.CAR, "C-1"), at(9))
    check("hourly fee before swap", lot.exit(tk_a.ticket_id, at(12)), 3)
    tk_b = lot.entry(Vehicle(VehicleType.CAR, "C-2"), at(9))
    lot.set_pricing_strategy(WeekendRates())
    check("same car, same stay, weekend fee after swap", lot.exit(tk_b.ticket_id, at(12)), 4.5)
    tk_c = lot.entry(Vehicle(VehicleType.CAR, "C-3"), at(9))
    lot.set_pricing_strategy(HourlyRates())
    check("swapping back restores hourly fee", lot.exit(tk_c.ticket_id, at(12)), 3)