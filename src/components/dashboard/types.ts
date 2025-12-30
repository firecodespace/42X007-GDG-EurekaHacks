export type EventOrganizer = {
    name: string;
};

export type Event = {
    id: string;
    title: string;
    description: string;
    location: string;
    aiFitScore: number; // 0-100
    organizers: EventOrganizer[];
    memberRangeLabel: string; // e.g. "1-4 members"
    cta: {
        primaryLabel: string; // e.g. "Register"
        href: string; // e.g. "/events/123/register"
        secondaryLabel?: string; // e.g. "View info"
        secondaryHref?: string;
    };
};
