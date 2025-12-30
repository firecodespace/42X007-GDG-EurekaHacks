import type { Event } from "./types";
import { EventRail } from "./EventRail";

type EventRailSectionProps = {
    title: string;
    events: Event[];
    insetClassName?: string; // must match EventRail inset
};

export function EventRailSection({
    title,
    events,
    insetClassName = "px-6 sm:px-10 lg:px-14",
}: EventRailSectionProps) {
    if (!events?.length) return null;

    return (
        <section className="space-y-5">
            {/* Full-bleed title so it aligns with a full-bleed rail */}
            <div className="relative left-1/2 w-screen -translate-x-1/2">
                <div className={insetClassName}>
                    <h3 className="text-2xl font-semibold tracking-tight text-white">
                        {title}
                    </h3>
                </div>
            </div>

            <EventRail events={events} insetClassName={insetClassName} />
        </section>
    );
}
