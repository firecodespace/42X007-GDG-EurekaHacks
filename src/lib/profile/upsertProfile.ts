import { auth, db } from "@/lib/auth/firebaseClient";
import { doc, serverTimestamp, setDoc } from "firebase/firestore";
import type { OnboardingDraft } from "@/lib/onboarding/store";

export async function upsertUserProfileFromDraft(draft: OnboardingDraft) {
    const user = auth.currentUser;
    if (!user) throw new Error("Not signed in.");

    const ref = doc(db, "users", user.uid);

    await setDoc(
        ref,
        {
            uid: user.uid,
            name: draft.name || user.displayName || "",
            email: draft.email || user.email || "",
            phone: draft.phone || user.phoneNumber || "",
            university: draft.university,
            course: draft.course,
            username: draft.username,
            googleConnected: draft.googleConnected,
            onboardingComplete: true,
            updatedAt: serverTimestamp(),
            createdAt: serverTimestamp(),
        },
        { merge: true }
    );
}
