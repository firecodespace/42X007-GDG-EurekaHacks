import { IntroHero } from "@/components/dashboard/IntroHero";
import { EventRailSection } from "@/components/dashboard/EventRailSection";
import { mockEvents } from "@/components/dashboard/mock/events";

export default function HomePage() {
  return (
    <main className="min-h-dvh px-6 py-10 text-white">
      <div className="mx-auto w-full max-w-6xl space-y-14">
        <h1 className="text-3xl font-semibold">HackFlix</h1>

        <IntroHero
          title="A Personalized AI System That Learns Your Skills and Maps You to the Right Opportunities"
          subtitle="Tell HackFlix what you’re good at, what you want to build, and the time you can commit—then get events and hackathons ranked by fit score, team size, and organizer quality."
          primaryCta={{ label: "Build my profile", href: "/onboarding" }}
          secondaryCta={{ label: "See recommendations", href: "/dashboard" }}
        />

        <EventRailSection title="Hackathons in Noida" events={mockEvents} />
      </div>
    </main>
  );
}
