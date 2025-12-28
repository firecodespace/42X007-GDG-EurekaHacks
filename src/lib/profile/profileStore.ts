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
    updatedAt?: number;
};

export async function getUserProfile(uid: string): Promise<UserProfile | null> {
    try {
        const ref = doc(db, "users", uid);
        const snap = await getDoc(ref); // [web:610]
        return snap.exists() ? (snap.data() as UserProfile) : null;
    } catch (e) {
        console.error("getUserProfile failed:", e);
        throw e;
    }
}

export function isProfileComplete(p: UserProfile) {
    return Boolean(
        p.name?.trim() &&
        p.email?.trim() &&
        p.phone?.trim() &&
        p.university?.trim() &&
        p.course?.trim() &&
        p.username?.trim()
    );
}
