// src/app/onboarding/review/page.tsx
"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useOnboarding } from "@/lib/onboarding/store";
import { useAuthUser } from "@/lib/auth/useAuthUser";
import { getAuth } from "firebase/auth";
import { doc, setDoc, serverTimestamp } from "firebase/firestore";
import { db } from "@/lib/auth/firebaseClient";

export default function OnboardingReviewPage() {
    const router = useRouter();
    const { draft, reset } = useOnboarding();
    const { user, loading, signedIn } = useAuthUser();
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const canFinish = signedIn && !loading && !busy && user?.uid;

    const handleFinish = async () => {
        if (!canFinish || !user?.uid) return;

        setBusy(true);
        setError(null);

        try {
            // Direct Firestore write - no missing imports
            await setDoc(
                doc(db, "users", user.uid),
                {
                    uid: user.uid,
                    name: draft.name,
                    email: draft.email,
                    phone: draft.phone,
                    university: draft.university,
                    course: draft.course,
                    username: draft.username,
                    googleConnected: draft.googleConnected,
                    updatedAt: serverTimestamp(),
                    createdAt: serverTimestamp(),
                },
                { merge: true }
            );

            reset();
            router.push("/profile");
        } catch (e: any) {
            setError(e.message || "Failed to save profile");
        } finally {
            setBusy(false);
        }
    };

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
                    <Row k="Google" v={draft.googleConnected ? "Yes" : "No"} />
                </div>

                {error && <div className="mt-6 text-red-300">{error}</div>}
                {!signedIn && !loading && (
                    <div className="mt-4 text-red-300 text-sm">
                        Please complete phone verification first
                    </div>
                )}

                <div className="mt-8 sm:mt-10 flex items-center justify-end gap-4 sm:gap-5">
                    <button
                        type="button"
                        onClick={() => router.back()}
                        disabled={busy}
                        className="cursor-pointer p-3 sm:p-2 text-white/80 hover:text-white disabled:opacity-30"
                    >
                        <ArrowLeft className="h-6 w-6 sm:h-7 sm:w-7" />
                    </button>

                    <button
                        type="button"
                        disabled={!canFinish}
                        onClick={handleFinish}
                        className="cursor-pointer p-3 sm:p-2 text-white/90 hover:text-white disabled:opacity-30"
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
