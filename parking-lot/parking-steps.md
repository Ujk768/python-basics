Let’s do a Parking Lot. It reuses what you just learned (registry-style tracking, Strategy for pricing, state transitions) and adds two new skills: choosing between inheritance and composition, and allocation logic.
## Problem: Multi-Level Parking Lot
# Requirements

The lot has multiple floors, and each floor has multiple spots.
Spots come in sizes: MOTORCYCLE, COMPACT, LARGE. Vehicles come in types: MOTORCYCLE, CAR, TRUCK.
Fit rules: a motorcycle fits any spot, a car fits COMPACT or LARGE, a truck fits only LARGE.
When a vehicle enters, the lot assigns a spot and issues a Ticket (ticket ID, vehicle, spot, entry time).
When a vehicle exits, the ticket is closed, a fee is calculated from the duration, and the spot is freed.
Pricing must be swappable: hourly rate per vehicle type now, with something like a daily cap or weekend rates later, without editing existing classes.
If no suitable spot exists, entry fails clearly.

# Constraints

- A vehicle can’t enter twice without exiting.
- Exiting with an invalid or already-used ticket must fail.
- Spot assignment strategy should be swappable too (e.g. nearest to entrance vs. lowest floor first).

# 1. Who picks the spot? (needs a tweak)

ParkingLot has the data, but requirement 8 says the assignment strategy must be swappable. If ParkingLot owns the “nearest to entrance” logic, swapping it means editing ParkingLot, which is exactly what the Strategy pattern from last time was meant to avoid. A better split is that ParkingLot orchestrates (entry, exit, tickets) and delegates “which spot?” to a separate allocation strategy. The strategy receives the floors and the vehicle and returns a spot or nothing. Rewrite your answer with that split in mind.

# 2. Vehicle as one class plus enum (good)
Your reasoning holds: vehicles differ in data, not behavior, so subclasses would be empty shells. For the “what you lose” half, think about what happens when someone adds a new vehicle type later. Which places do you have to touch? Add that sentence to your answer.

# 3. Where does “does it fit?” live? (not yet)
Floor is a shaky home. The allocator also needs this rule while scanning spots across floors, so it would have to reach through Floor for something that is really about one vehicle and one spot. Ask yourself which single object knows both the vehicle’s type and the spot’s size, and where one table (vehicle type to allowed spot sizes) could live so the rule is defined exactly once. Then give me your revised answer.

# 4. Tracking who’s inside (good, one gap)
A map keyed by vehicle number is the right instinct, and it’s the same idea as your loan registry. Two things to decide:

The exit rule needs a lookup by ticket ID, which is a different key. Do you need a second map, or can one structure serve both?
After exit, do you delete the ticket or keep it as closed? Your answer determines how “already-used ticket” gets detected.



## Who picks the spot to decide where to park the car

A ParkingSpot class owns its size, its floor, and whether it’s occupied, and has can_fit(vehicle).

One lookup table (vehicle type to allowed spot sizes) lives next to the enums, and can_fit reads from it.
Allocators loop over spots in their preferred order and return the first one where spot.is_free() and spot.can_fit(vehicle).

## Entities to be Used

- Vehicles owns vehicle details ( vehicleType, registration number)
- Floor owns the floor details (floor number, list of spots)
- Parking Lot (floors, vehicles, tikcets, clock)
- Ticket (id , spot_selcted,vehicle, entry_time )
- Alocation Stratergies (method - allocate which is implemented bny its own sub class)
- Pricing Stratergies (method - calculate price which is implented by its own pricce sub classes such as WeekendRates)
- Vehicle Type & Spot Size ( Enums)
- Parking Spot - (id, spot_size, can_fit(Vehicle))

- Parking Lot will hold 2 maps 
-> lookup by ticket_id 
-> lookup by vehicle number

idk what pattern this is called

This prevents same car from entering inside and at then end I can use ticket id to calculate the price to pay



## Tests
1. Motorcycle gets a LARGE spot when only LARGE is free, and a later truck is then refused.
2. Truck refused when only COMPACT spots are free: error, no ticket, no state change.
3. Same vehicle number enters twice without exiting: second entry fails.
4. exit with a ticket ID that never existed fails with an error -> ticket id doesnt exist
    second exit with same ticket will also fail with same error as we have closed that ticket
5. Exit frees the spot, and the next vehicle can take it.
6. Fee with exact numbers: a car for 3 hours at a rate you choose gives one specific amount. A partial Hour will be rounded up so for 3.5 hours at $1 per hr the total will be 3.5 *1 = 3.5 => 4 
7. Given a car that entered under hourly pricing, when the lot’s strategy is swapped to Weekend Rates before exit, then the car will pay new Weekend rate


