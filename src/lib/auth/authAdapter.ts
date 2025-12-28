import {
    GoogleAuthProvider,
    getAdditionalUserInfo,
    signInWithPopup,
} from "firebase/auth";
import { doc, setDoc } from "firebase/firestore";
import { auth, db } from "./firebaseClient";

export type GoogleProfile = {
    uid: string;
    name: string | null;
    email: string | null;
    phone: string | null;
    photoURL: string | null;
    isNewUser: boolean;
    accessToken: string | null;
};

export async function signInWithGoogle(): Promise<GoogleProfile> {
    const provider = new GoogleAuthProvider();
    provider.setCustomParameters({ prompt: "select_account" });

    const result = await signInWithPopup(auth, provider);
    const info = getAdditionalUserInfo(result);
    const credential = GoogleAuthProvider.credentialFromResult(result);

    const user = result.user;

    return {
        uid: user.uid,
        name: user.displayName ?? null,
        email: user.email ?? null,
        phone: user.phoneNumber ?? null,
        photoURL: user.photoURL ?? null,
        isNewUser: Boolean(info?.isNewUser),
        accessToken: credential?.accessToken ?? null,
    };
}

// ✅ ADD THIS EXPORT (so review/page.tsx can import it)
export async function persistProfile(draft: {
    name: string;
    email: string;
    phone: string;
    university: string;
    course: string;
    username: string;
    googleConnected: boolean;
}) {
    const user = auth.currentUser;
    if (!user) throw new Error("Not signed in");

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
            updatedAt: Date.now(),
        },
        { merge: true } // keeps existing fields [web:545]
    );
}
