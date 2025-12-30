import { IntroHero } from "@/components/dashboard/IntroHero";
import { EventRail } from "@/components/dashboard/EventRail";
import { mockEvents } from "@/components/dashboard/mock/events";

export default function HomePage() {
  return (
    <main className="min-h-dvh px-6 py-10 text-white">
      <div className="mx-auto w-full max-w-6xl space-y-12">
        <h1 className="text-3xl font-semibold">HackFlix</h1>

        <IntroHero
          title="A Personalized AI System That Learns Your Skills and Maps You to the Right Opportunities"
          subtitle="Tell HackFlix what you are good at, what you want to build, and what you have already built, then get events and hackathons recommendations ranked by fit score, team size, and organizer quality."
          primaryCta={{ label: "Build my profile", href: "/onboarding" }}
          secondaryCta={{ label: "See recommendations", href: "/dashboard" }}
        />

        {/* Bigger gap before cards */}
        <div className="mt-10 sm:mt-14 lg:mt-16">
          <EventRail events={mockEvents} />
        </div>
      </div>
    </main>
  );
}
