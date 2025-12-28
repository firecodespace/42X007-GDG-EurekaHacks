import type { OnboardingDraft } from "@/types/onboarding";

export type GoogleAuthResult = {
    name?: string;
    email?: string;
    phone?: string;
    photoUrl?: string;
};

export async function signInWithGoogle(): Promise<GoogleAuthResult> {
    return {
        name: "Google User",
        email: "user@gmail.com",
    };
}

export async function signUpWithEmailPassword(_email: string, _password: string) {
    return;
}

export async function persistProfile(_draft: OnboardingDraft) {
    return;
}
