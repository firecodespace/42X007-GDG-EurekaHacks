// src/lib/profile/profileStore.ts
import { doc, getDoc } from "firebase/firestore";
import { db } from "@/lib/auth/firebaseClient";

export type UserProfile = {
    uid: string;
    name?: string;
    email?: string;
    phone?: string;
    university?: string;
    course?: string;
    username?: string;
    googleConnected?: boolean;
};

export async function getUserProfile(uid: string): Promise<UserProfile | null> {
    try {
        const snap = await getDoc(doc(db, "users", uid));
        if (snap.exists()) {
            return { uid, ...snap.data() } as UserProfile;
        }
        return null;
    } catch {
        return null;
    }
}

export function isProfileComplete(p: UserProfile): boolean {
    return Boolean(
        p.name?.trim() &&
        p.email?.trim() &&
        p.phone?.trim() &&
        p.university?.trim() &&
        p.course?.trim() &&
        p.username?.trim()
    );
}
