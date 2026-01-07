// src/lib/auth/authAdapter.ts
import {
    GoogleAuthProvider,
    getAdditionalUserInfo,
    signInWithPopup,
} from "firebase/auth";
import { auth } from "./firebaseClient";

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
