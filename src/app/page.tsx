import { IntroHero } from "@/components/dashboard/IntroHero";
import { EventRailSection } from "@/components/dashboard/EventRailSection";
import { mockEvents } from "@/components/dashboard/mock/events";
import { Navbar } from "@/components/dashboard/navbar/Navbar";

export default function HomePage() {
  return (
    <main className="min-h-dvh text-white">
      <Navbar />
      <div className="mx-auto w-full max-w-6xl space-y-14">
        <IntroHero
          title="A Personalized AI System That Learns Your Skills and Maps You to the Right Opportunities"
          subtitle="Tell HackFlix what you’re good at, what you want to build, and the time you can commit, then get events and hackathons ranked by fit score, team size, and organizer quality."
          primaryCta={{ label: "Build my profile", href: "/onboarding" }}
          secondaryCta={{ label: "See recommendations", href: "/dashboard" }}
        />

        <EventRailSection title="Hackathons in Noida" events={mockEvents} />
      </div>
    </main>
  );
}
