import { doc, getDoc } from "firebase/firestore";
import { db } from "@/lib/auth/firebaseClient";

export type UserProfile = {
    uid: string;
    name: string;
    email: string;
    phone: string;
    university: string;
    course: string;
    username: string;
    googleConnected: boolean;
    updatedAt: number;
};

export async function getUserProfile(uid: string): Promise<UserProfile | null> {
    const snap = await getDoc(doc(db, "users", uid));
    return snap.exists() ? (snap.data() as UserProfile) : null;
}
