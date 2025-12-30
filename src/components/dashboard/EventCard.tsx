import type { Event } from "./types";
import { CardShell } from "@/components/ui/CardShell";
import { Button } from "@/components/ui/Button";

function PinIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
                d="M12 22s7-4.5 7-11a7 7 0 1 0-14 0c0 6.5 7 11 7 11Z"
                stroke="currentColor"
                strokeWidth="1.8"
            />
            <path
                d="M12 11.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z"
                stroke="currentColor"
                strokeWidth="1.8"
            />
        </svg>
    );
}

function SparkleIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
                d="M12 2l1.2 4.2L17 7.5l-3.8 1.3L12 13l-1.2-4.2L7 7.5l3.8-1.3L12 2Z"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinejoin="round"
            />
        </svg>
    );
}

function PeopleIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
                d="M16 19c0-2.2-1.8-4-4-4s-4 1.8-4 4"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
            />
            <path
                d="M12 13a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z"
                stroke="currentColor"
                strokeWidth="1.8"
            />
        </svg>
    );
}

function OrganizerIcon() {
    return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
                d="M4 21V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v13"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
            />
            <path
                d="M9 21v-6h6v6"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
            />
            <path
                d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
            />
        </svg>
    );
}

export function EventCard({ event }: { event: Event }) {
    const score = Math.max(0, Math.min(100, Math.round(event.aiFitScore)));

    const organizersLabel =
        event.organizers.length === 0
            ? "event organizers"
            : event.organizers.length === 1
                ? event.organizers[0].name
                : `${event.organizers[0].name}`;

    return (
        <CardShell>
            <div className="flex h-full flex-col">
                {/* Top */}
                <div className="space-y-4">
                    <h3 className="text-[28px] font-semibold leading-tight text-white">
                        {event.title}
                    </h3>

                    <p className="text-[16px] leading-[26px] text-white/75 line-clamp-4">
                        {event.description}
                    </p>
                </div>

                {/* Middle metadata (positioned like the image: grouped, with spacing) */}
                <div className="mt-7 space-y-3 text-white/80">
                    <div className="flex items-center gap-2">
                        <span className="text-white/70">
                            <PinIcon />
                        </span>
                        <span className="text-[18px] leading-none">{event.location}</span>
                    </div>

                    <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-2">
                            <span className="text-white/70">
                                <SparkleIcon />
                            </span>
                            <span className="text-[18px] leading-none">
                                AI fit score{" "}
                                <span className="text-[#9AFFF7]">{score}%</span>
                            </span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <span className="text-white/70">
                            <OrganizerIcon />
                        </span>
                        <span className="text-[18px] leading-none">{organizersLabel}</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <span className="text-white/70">
                            <PeopleIcon />
                        </span>
                        <span className="text-[18px] leading-none">{event.memberRangeLabel}</span>
                    </div>
                </div>

                {/* Bottom CTAs */}
                <div className="mt-auto flex items-end justify-between gap-6 pt-8">
                    {event.cta.secondaryLabel && event.cta.secondaryHref ? (
                        <Button href={event.cta.secondaryHref} variant="ghost" className="h-[45px]">
                            {event.cta.secondaryLabel}
                        </Button>
                    ) : (
                        <span />
                    )}

                    <Button href={event.cta.href} className="min-w-[150px]">
                        {event.cta.primaryLabel}
                    </Button>
                </div>
            </div>
        </CardShell>
    );
}
