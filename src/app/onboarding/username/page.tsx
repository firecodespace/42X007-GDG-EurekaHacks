"use client";

import { useRouter } from "next/navigation";
import UnderlineStep from "@/app/onboarding/_components/UnderlineStep";
import { useOnboarding } from "@/lib/onboarding/store";

export default function OnboardingUsernamePage() {
    const router = useRouter();
    const { draft, setDraft } = useOnboarding();

    const canContinue = draft.username.trim().length >= 3;

    return (
        <main className="min-h-dvh px-5 sm:px-8 lg:px-10 py-10 sm:py-14 lg:py-16 text-white">
            <div className="max-w-5xl">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight">
                    Username
                </h1>
                <p className="mt-3 sm:mt-4 text-lg sm:text-xl lg:text-2xl text-white/70">
                    Visible on your profile.
                </p>

                <div className="mt-10 sm:mt-14">
                    <UnderlineStep
                        label="Set a username"
                        value={draft.username}
                        onChange={(v) => setDraft((p) => ({ ...p, username: v }))}
                        canContinue={canContinue}
                        onContinue={() => router.push("/onboarding/review")}
                        onBack={() => router.back()}
                    />
                </div>
            </div>
        </main>
    );
}
