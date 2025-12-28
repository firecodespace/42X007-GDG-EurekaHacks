"use client";

import { useRouter } from "next/navigation";
import { ArrowRight } from "lucide-react";
import { useState } from "react";
import { useOnboarding } from "@/lib/onboarding/store";
import { signInWithGoogle } from "@/lib/auth/authAdapter";

export default function OnboardingNamePage() {
    const router = useRouter();
    const { draft, setDraft } = useOnboarding();
    const [busy, setBusy] = useState(false);

    const canContinue = draft.name.trim().length >= 2;

    function next() {
        if (!canContinue) return;
        router.push("/onboarding/email");
    }

    return (
        <main className="min-h-dvh px-10 py-16 text-white">
            <div className="max-w-5xl">
                <h1 className="text-6xl font-semibold tracking-tight">Welcome to HackFlix</h1>
                <p className="mt-4 text-2xl text-white/70">Setup your profile, answer the questions.</p>

                <div className="mt-14">
                    <label className="block text-white/90 text-3xl">What should we call you?</label>

                    <div className="mt-10 flex items-end gap-4">
                        <input
                            autoFocus
                            value={draft.name}
                            onChange={(e) => setDraft((p) => ({ ...p, name: e.target.value }))}
                            onKeyDown={(e) => {
                                if (e.key !== "Enter") return;
                                e.preventDefault();
                                next();
                            }}
                            className="w-full bg-transparent text-white text-4xl outline-none"
                        />

                        <button
                            type="button"
                            aria-label="Continue"
                            onClick={next}
                            disabled={!canContinue || busy}
                            className="cursor-pointer flex h-12 w-12 items-center justify-center rounded-full border border-white/25 text-white disabled:cursor-not-allowed disabled:opacity-40"
                        >
                            <ArrowRight className="h-5 w-5" />
                        </button>
                    </div>

                    <div className="mt-6 h-px w-full bg-white/30" />
                </div>

                <div className="mt-14 text-2xl text-white/70">or continue with your Google account</div>

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
                    className="cursor-pointer mt-6 flex h-12 w-full max-w-md items-center justify-center rounded-xl bg-white px-6 text-base font-medium text-black disabled:cursor-not-allowed disabled:opacity-50"
                >
                    Continue with Google
                </button>
            </div>
        </main>
    );
}
