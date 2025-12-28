"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useOnboarding } from "@/lib/onboarding/store";
import { persistProfile } from "@/lib/auth/authAdapter";

export default function OnboardingReviewPage() {
    const router = useRouter();
    const { draft } = useOnboarding();
    const [busy, setBusy] = useState(false);

    return (
        <main className="min-h-dvh px-5 sm:px-8 lg:px-10 py-10 sm:py-14 lg:py-16 text-white">
            <div className="max-w-5xl">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight">
                    Review
                </h1>
                <p className="mt-3 sm:mt-4 text-lg sm:text-xl lg:text-2xl text-white/70">
                    Confirm your details.
                </p>

                <div className="mt-10 sm:mt-14 rounded-2xl border border-white/15 bg-black/20 backdrop-blur-md p-4 sm:p-6">
                    <Row k="Name" v={draft.name || "—"} />
                    <Row k="Email" v={draft.email || "—"} />
                    <Row k="Phone" v={draft.phone || "—"} />
                    <Row k="University" v={draft.university || "—"} />
                    <Row k="Course" v={draft.course || "—"} />
                    <Row k="Username" v={draft.username || "—"} />
                </div>

                <div className="mt-8 sm:mt-10 flex items-center justify-end gap-4 sm:gap-5">
                    <button
                        type="button"
                        aria-label="Back"
                        onClick={() => router.back()}
                        disabled={busy}
                        className="cursor-pointer p-3 sm:p-2 text-white/80 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
                    >
                        <ArrowLeft className="h-6 w-6 sm:h-7 sm:w-7" />
                    </button>

                    <button
                        type="button"
                        aria-label="Finish"
                        disabled={busy}
                        onClick={async () => {
                            setBusy(true);
                            try {
                                await persistProfile(draft as any);
                                router.push("/profile");
                            } finally {
                                setBusy(false);
                            }
                        }}
                        className="cursor-pointer p-3 sm:p-2 text-white/90 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
                    >
                        <ArrowRight className="h-6 w-6 sm:h-7 sm:w-7" />
                    </button>
                </div>
            </div>
        </main>
    );
}

function Row({ k, v }: { k: string; v: string }) {
    return (
        <div className="flex items-center justify-between gap-6 py-2">
            <div className="text-white/70 text-sm sm:text-base">{k}</div>
            <div className="text-white text-sm sm:text-base">{v}</div>
        </div>
    );
}
