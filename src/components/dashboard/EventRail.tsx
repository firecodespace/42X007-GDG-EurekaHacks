import type { Event } from "./types";
import { EventCard } from "./EventCard";

type EventRailProps = {
    events: Event[];
    insetClassName?: string;
};

export function EventRail({
    events,
    insetClassName = "px-6 sm:px-10 lg:px-14",
}: EventRailProps) {
    return (
        <section className="relative left-1/2 w-screen -translate-x-1/2">
            <div
                className={[
                    "overflow-x-auto overflow-y-hidden scroll-smooth",
                    "[scrollbar-width:none]",
                    "[-ms-overflow-style:none]",
                    "[&::-webkit-scrollbar]:hidden",
                ].join(" ")}
            >
                <div className={["flex w-max items-stretch gap-10", insetClassName, "snap-x snap-mandatory"].join(" ")}>
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
