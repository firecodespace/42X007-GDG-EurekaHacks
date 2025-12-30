import { mockEvents } from "@/components/dashboard/mock/events";
import { EventRail } from "@/components/dashboard/EventRail";

export default function HomePage() {
  return (
    <main className="min-h-dvh px-6 py-10 text-white">
      <div className="mx-auto w-full max-w-6xl space-y-10">
        <h1 className="text-3xl font-semibold">HackFlix</h1>
        <EventRail events={mockEvents} />
      </div>
    </main>
  );
}
