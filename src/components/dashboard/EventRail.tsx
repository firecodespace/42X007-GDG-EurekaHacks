import type { Event } from "./types";
import { EventCard } from "./EventCard";

export function EventRail({ events }: { events: Event[] }) {
    return (
        // Full-bleed: this ignores parent max-width and becomes full viewport width.
        <section className="relative left-1/2 w-screen -translate-x-1/2">
            <div
                className={[
                    "overflow-x-auto overflow-y-hidden scroll-smooth",
                    // Hide scrollbar everywhere
                    "[scrollbar-width:none]",
                    "[-ms-overflow-style:none]",
                    "[&::-webkit-scrollbar]:hidden",
                ].join(" ")}
            >
                <div
                    className={[
                        "flex w-max items-stretch gap-10",
                        // This is the "gap from left side" you asked:
                        // responsive left/right padding so it looks premium on all screens.
                        "px-6 sm:px-10 lg:px-14",
                        // Snap makes the scroll feel intentional
                        "snap-x snap-mandatory",
                    ].join(" ")}
                >
                    {events.map((event) => (
                        <div key={event.id} className="snap-start">
                            <div className="w-[min(400px,calc(100vw-48px))]">
                                <EventCard event={event} />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
