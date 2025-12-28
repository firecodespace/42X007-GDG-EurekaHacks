"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function OnboardingIntroPage() {
    const router = useRouter();
    const [busy, setBusy] = useState(false);

    return (
        <main className="min-h-dvh px-5 sm:px-8 lg:px-10 py-10 sm:py-14 lg:py-16 text-white">
            <div className="max-w-5xl">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight">
                    Let’s set up your account
                </h1>
                <p className="mt-3 sm:mt-4 text-lg sm:text-xl lg:text-2xl text-white/70">
                    This takes under a minute. You’ll add your basics, then you’re in.
                </p>

                <div className="mt-10 sm:mt-12 rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-7">
                    <div className="text-base sm:text-lg text-white/80">
                        What you’ll do:
                    </div>
                    <ul className="mt-4 space-y-2 text-sm sm:text-base text-white/70">
                        <li>• Choose a name & confirm email.</li>
                        <li>• Add university, course, and a username.</li>
                        <li>• Finish and land on your profile.</li>
                    </ul>

                    <div className="mt-6 text-sm sm:text-base text-white/60">
                        Tip: If you’ve already completed onboarding before, Google sign-in will skip steps and take you straight to profile.
                    </div>
                </div>

                <div className="mt-10 flex flex-col gap-3 sm:flex-row sm:items-center">
                    <button
                        type="button"
                        disabled={busy}
                        onClick={() => {
                            if (busy) return;
                            setBusy(true);
                            router.push("/onboarding/name");
                        }}
                        className="cursor-pointer inline-flex h-11 sm:h-12 w-full sm:w-auto items-center justify-center rounded-xl bg-white px-6 text-sm sm:text-base font-medium text-black disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {busy ? "Starting..." : "Continue"}
                    </button>

                    <button
                        type="button"
                        disabled={busy}
                        onClick={() => router.push("/")}
                        className="cursor-pointer inline-flex h-11 sm:h-12 w-full sm:w-auto items-center justify-center rounded-xl border border-white/15 bg-transparent px-6 text-sm sm:text-base font-medium text-white/90 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        Back
                    </button>
                </div>
            </div>
        </main>
    );
}
