// src/lib/profile/upsertProfile.ts
import { doc, setDoc, serverTimestamp } from "firebase/firestore";
import { db } from "@/lib/auth/firebaseClient";
import type { OnboardingDraft } from "@/lib/onboarding/store";
import { useAuthUser } from "@/lib/auth/useAuthUser";

export async function upsertUserProfileFromDraft(draft: OnboardingDraft) {
    // Get current user from auth
    const { user } = useAuthUser();
    if (!user?.uid) throw new Error("No authenticated user");

    await setDoc(
        doc(db, "users", user.uid),
        {
            uid: user.uid,
            ...draft,
            updatedAt: serverTimestamp(),
            createdAt: serverTimestamp(),
        },
        { merge: true }
    );
}
