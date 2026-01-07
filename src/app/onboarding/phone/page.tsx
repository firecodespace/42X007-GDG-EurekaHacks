// src/app/onboarding/phone/page.tsx
"use client";

import { useMemo, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ConfirmationResult } from "firebase/auth";

import UnderlineStep from "../_components/UnderlineStep";
import { useOnboarding } from "@/lib/onboarding/store";
import { sendOtp, verifyOtp, cleanupRecaptcha } from "@/lib/auth/phoneOtp";

function toE164India(raw: string) {
    const digits = raw.replace(/\D/g, "");
    if (raw.trim().startsWith("+")) return `+${digits}`;
    if (digits.startsWith("91") && digits.length >= 12) return `+${digits}`;
    return `+91${digits}`;
}

export default function OnboardingPhonePage() {
    const router = useRouter();
    const { draft, setDraft } = useOnboarding();

    const [busy, setBusy] = useState(false);
    const [mode, setMode] = useState<"phone" | "otp">("phone");
    const [otp, setOtp] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [confirmation, setConfirmation] = useState<ConfirmationResult | null>(null);

    const phoneE164 = useMemo(() => toE164India(draft.phone || ""), [draft.phone]);
    const canSendOtp = draft.phone.trim().length >= 10 && !busy;
    const canVerifyOtp = otp.trim().length >= 6 && !!confirmation && !busy;

    // Cleanup on unmount
    useEffect(() => {
        return () => cleanupRecaptcha();
    }, []);

    const handleSendOtp = async () => {
        if (!canSendOtp) return;

        setBusy(true);
        setError(null);

        try {
            const c = await sendOtp(phoneE164, "recaptcha-container");
            setConfirmation(c);
            setMode("otp"); // Switch to OTP mode
            setOtp("");
        } catch (e: any) {
            console.error("Send OTP error:", e);
            setError(e.message || "Failed to send OTP. Check Firebase Console.");
        } finally {
            setBusy(false);
        }
    };

    const handleVerifyOtp = async () => {
        if (!confirmation || !canVerifyOtp) return;

        setBusy(true);
        setError(null);

        try {
            await verifyOtp(confirmation, otp.trim());
            router.push("/onboarding/university");
        } catch (e: any) {
            console.error("Verify OTP error:", e);
            setError(e.message || "Invalid OTP code");
            setOtp("");
        } finally {
            setBusy(false);
        }
    };

    return (
        <main className="min-h-dvh px-5 sm:px-8 lg:px-10 py-10 sm:py-14 lg:py-16 text-white">
            {/* CRITICAL: Container must exist BEFORE first sendOtp call */}
            <div id="recaptcha-container" className="fixed top-0 left-0 z-50" />

            <div className="max-w-5xl">
                {mode === "phone" ? (
                    <>
                        <UnderlineStep
                            label="Your phone number"
                            value={draft.phone}
                            onChange={(v) => {
                                setError(null);
                                setDraft((prev) => ({ ...prev, phone: v }));
                            }}
                            inputMode="tel"
                            canContinue={canSendOtp}
                            onContinue={handleSendOtp}
                            onBack={() => router.back()}
                            disabled={busy}
                        />

                        {error && (
                            <div className="mt-6 p-4 rounded-xl bg-red-500/20 border border-red-500/50 text-red-200 text-sm">
                                ⚠️ {error}
                            </div>
                        )}

                        <div className="mt-6 text-white/60 text-sm">
                            OTP will be sent to: <span className="text-white font-medium">{phoneE164}</span>
                        </div>
                    </>
                ) : (
                    <>
                        <div className="mb-8">
                            <h2 className="text-2xl font-semibold">Enter OTP</h2>
                            <p className="mt-2 text-white/70">
                                6-digit code sent to {phoneE164}
                            </p>
                        </div>

                        <UnderlineStep
                            label="OTP Code"
                            value={otp}
                            onChange={(v) => {
                                setError(null);
                                // Only allow numbers, max 6 digits
                                const clean = v.replace(/\D/g, "").slice(0, 6);
                                setOtp(clean);
                            }}
                            inputMode="numeric"
                            canContinue={canVerifyOtp}
                            onContinue={handleVerifyOtp}
                            onBack={() => {
                                setMode("phone");
                                setOtp("");
                                setConfirmation(null);
                                setError(null);
                            }}
                            disabled={busy}
                        />

                        {error && (
                            <div className="mt-6 p-4 rounded-xl bg-red-500/20 border border-red-500/50 text-red-200 text-sm">
                                ⚠️ {error}
                            </div>
                        )}

                        <div className="mt-8 text-center">
                            <button
                                type="button"
                                disabled={busy}
                                onClick={() => {
                                    setMode("phone");
                                    setOtp("");
                                    setConfirmation(null);
                                }}
                                className="text-white/70 hover:text-white underline disabled:opacity-50"
                            >
                                Change phone number
                            </button>
                        </div>
                    </>
                )}

                {busy && (
                    <div className="mt-6 flex items-center gap-3 text-white/60">
                        <div className="h-5 w-5 rounded-full border-2 border-white/30 border-t-white animate-spin" />
                        <span>{mode === "phone" ? "Sending OTP..." : "Verifying..."}</span>
                    </div>
                )}
            </div>
        </main>
    );
}
