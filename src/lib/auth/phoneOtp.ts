// src/lib/auth/phoneOtp.ts
"use client";

import {
    ConfirmationResult,
    RecaptchaVerifier,
    signInWithPhoneNumber,
} from "firebase/auth";
import { auth } from "./firebaseClient";

let verifier: RecaptchaVerifier | null = null;

export function initRecaptcha(containerId: string): RecaptchaVerifier {
    // CRITICAL: Don't recreate if exists
    if (verifier) {
        try {
            verifier.clear();
        } catch {
            // Ignore if already cleared
        }
    }

    verifier = new RecaptchaVerifier(auth, containerId, {
        size: "invisible",
        callback: () => {
            console.log("reCAPTCHA solved");
        },
    });

    return verifier;
}

export async function sendOtp(
    phoneE164: string,
    containerId: string
): Promise<ConfirmationResult> {
    try {
        const appVerifier = initRecaptcha(containerId);
        const confirmation = await signInWithPhoneNumber(auth, phoneE164, appVerifier);
        return confirmation;
    } catch (error: any) {
        // Cleanup on error
        if (verifier) {
            try {
                verifier.clear();
            } catch { }
            verifier = null;
        }
        throw error;
    }
}

export async function verifyOtp(
    confirmation: ConfirmationResult,
    code: string
) {
    const cred = await confirmation.confirm(code);

    // Cleanup after success
    if (verifier) {
        try {
            verifier.clear();
        } catch { }
        verifier = null;
    }

    return cred.user;
}

export function cleanupRecaptcha() {
    if (verifier) {
        try {
            verifier.clear();
        } catch { }
        verifier = null;
    }
}
