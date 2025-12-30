import { Button } from "@/components/ui/Button";

type IntroHeroProps = {
    title: string;
    subtitle: string;
    primaryCta?: { label: string; href: string };
    secondaryCta?: { label: string; href: string };
};

export function IntroHero({
    title,
    subtitle,
    primaryCta = { label: "Get matched", href: "/onboarding" },
    secondaryCta = { label: "Explore events", href: "/events" },
}: IntroHeroProps) {
    return (
        <section className="w-full">
            {/* Adds “centered” whitespace around hero */}
            <div className="mx-auto w-full max-w-6xl px-2 py-25 sm:py-25 lg:py-35">
                <div className="text-center">
                    <h2 className="mx-auto max-w-6xl text-balance text-3xl font-semibold leading-tight text-white sm:text-5xl sm:leading-tight">
                        {title}
                    </h2>

                    <p className="mx-auto mt-6 max-w-3xl text-pretty text-sm leading-7 text-white/75 sm:text-base">
                        {subtitle}
                    </p>

                    <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row sm:gap-6">
                        <Button href={primaryCta.href} className="min-w-[220px]">
                            {primaryCta.label}
                        </Button>

                        <Button href={secondaryCta.href} variant="ghost" className="min-w-[220px]">
                            {secondaryCta.label}
                        </Button>
                    </div>
                </div>
            </div>
        </section>
    );
}
