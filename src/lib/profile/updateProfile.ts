// src/lib/profile/updateProfile.ts
import { doc, updateDoc } from "firebase/firestore";
import { db } from "@/lib/auth/firebaseClient";

export async function updateProfileField(
    uid: string,
    field: string,
    value: any
) {
    await updateDoc(doc(db, "users", uid), {
        [field]: value,
    });
}

export async function addToArray(
    uid: string,
    field: string,
    item: any
) {
    const docRef = doc(db, "users", uid);
    const currentDoc = await import("firebase/firestore").then((mod) =>
        mod.getDoc(docRef)
    );
    const current = currentDoc.data()?.[field] || [];
    await updateDoc(docRef, {
        [field]: [...current, item],
    });
}

export async function removeFromArray(
    uid: string,
    field: string,
    index: number
) {
    const docRef = doc(db, "users", uid);
    const currentDoc = await import("firebase/firestore").then((mod) =>
        mod.getDoc(docRef)
    );
    const current = currentDoc.data()?.[field] || [];
    current.splice(index, 1);
    await updateDoc(docRef, {
        [field]: current,
    });
}
