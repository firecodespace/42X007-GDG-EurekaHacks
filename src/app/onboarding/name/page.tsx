"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import UnderlineStep from "@/app/onboarding/_components/UnderlineStep";
import { useOnboarding } from "@/lib/onboarding/store";
import { signInWithGoogle } from "@/lib/auth/authAdapter";

export default function OnboardingNamePage() {
    const router = useRouter();
    const { draft, setDraft } = useOnboarding();
    const [busy, setBusy] = useState(false);

    const canContinue = draft.name.trim().length >= 2;

    return (
        <main className="min-h-dvh px-5 sm:px-8 lg:px-10 py-10 sm:py-14 lg:py-16 text-white">
            <div className="max-w-5xl">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight">
                    Welcome to HackFlix
                </h1>
                <p className="mt-3 sm:mt-4 text-lg sm:text-xl lg:text-2xl text-white/70">
                    Setup your profile, answer the questions.
                </p>

                <div className="mt-10 sm:mt-14">
                    <UnderlineStep
                        label="What should we call you?"
                        value={draft.name}
                        onChange={(v) => setDraft((p) => ({ ...p, name: v }))}
                        canContinue={canContinue}
                        onContinue={() => router.push("/onboarding/email")}
                        disabled={busy}
                        canBack={false}
                    />
                </div>

                <div className="mt-10 sm:mt-14">
                    <div className="text-base sm:text-lg lg:text-2xl text-white/70">
                        or continue with your Google account
                    </div>

                    <button
                        type="button"
                        disabled={busy}
                        onClick={async () => {
                            setBusy(true);
                            try {
                                const res = await signInWithGoogle();
                                setDraft((p) => ({
                                    ...p,
                                    googleConnected: true,
                                    name: res.name ?? p.name,
                                    email: res.email ?? p.email,
                                    phone: res.phone ?? p.phone,
                                }));
                                router.push("/onboarding/email");
                            } finally {
                                setBusy(false);
                            }
                        }}
                        className="cursor-pointer mt-5 sm:mt-6 inline-flex h-11 sm:h-12 w-full max-w-md items-center justify-center rounded-xl bg-white px-6 text-sm sm:text-base font-medium text-black disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        Continue with Google
                    </button>
                </div>
            </div>
        </main>
    );
}
