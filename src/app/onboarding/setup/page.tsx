"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useOnboarding } from "@/lib/onboarding/store";
import { upsertUserProfileFromDraft } from "@/lib/profile/upsertProfile"; // you create this
import { useNavDirection } from "@/lib/onboarding/navDirection";

export default function OnboardingSetupPage() {
    const router = useRouter();
    const { draft, reset } = useOnboarding();
    const nav = useNavDirection();
    const [err, setErr] = useState<string | null>(null);

    useEffect(() => {
        nav.forward();

        (async () => {
            try {
                await upsertUserProfileFromDraft(draft);
                reset();
                router.replace("/profile");
            } catch (e: any) {
                setErr(e?.message ?? "Failed to set up profile.");
            }
        })();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <main className="min-h-dvh px-5 sm:px-8 lg:px-10 py-10 sm:py-14 lg:py-16 text-white">
            <div className="max-w-5xl">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight">
                    Setting up your profile
                </h1>
                <p className="mt-3 sm:mt-4 text-lg sm:text-xl lg:text-2xl text-white/70">
                    Just a moment. Finalizing your account details.
                </p>

                <div className="mt-10 sm:mt-14 rounded-2xl border border-white/10 bg-white/5 p-6 sm:p-8">
                    <div className="flex items-center gap-4">
                        <div className="h-10 w-10 rounded-full border border-white/15 flex items-center justify-center">
                            <div className="h-4 w-4 rounded-full border-2 border-white/30 border-t-white animate-spin" />
                        </div>
                        <div className="text-white/80">
                            Syncing data and preparing your profile…
                        </div>
                    </div>

                    {err ? (
                        <div className="mt-6 text-red-300">
                            {err}
                            <div className="mt-4 flex gap-3">
                                <button
                                    onClick={() => router.back()}
                                    className="h-11 rounded-xl border border-white/15 px-5 text-white/90"
                                >
                                    Go back
                                </button>
                                <button
                                    onClick={() => window.location.reload()}
                                    className="h-11 rounded-xl bg-white px-5 text-black font-medium"
                                >
                                    Retry
                                </button>
                            </div>
                        </div>
                    ) : null}
                </div>
            </div>
        </main>
    );
}
