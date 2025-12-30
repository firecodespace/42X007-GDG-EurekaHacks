import type { Event } from "./types";
import { EventRail } from "./EventRail";
import { CONTENT_INSET_CLASS } from "@/components/ui/layout";

type EventRailSectionProps = {
    title: string;
    events: Event[];
    insetClassName?: string;
};

export function EventRailSection({
    title,
    events,
    insetClassName = CONTENT_INSET_CLASS,
}: EventRailSectionProps) {
    if (!events?.length) return null;

    return (
        <section className="space-y-5">
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
