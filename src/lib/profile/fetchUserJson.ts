// src/lib/profile/fetchUserJson.ts
import { doc, getDoc } from "firebase/firestore";
import { db } from "@/lib/auth/firebaseClient";

export async function fetchUserJson(uid: string) {
    const snapshot = await getDoc(doc(db, "users", uid));
    if (!snapshot.exists()) return null;

    // Full JSON including the id
    return {
        id: snapshot.id,
        ...snapshot.data(),
    };
}
