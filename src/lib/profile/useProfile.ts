// src/lib/profile/useProfile.ts
"use client";

import { useEffect, useState } from "react";
import { doc, onSnapshot } from "firebase/firestore";
import { db } from "@/lib/auth/firebaseClient";
import { useAuthUser } from "@/lib/auth/useAuthUser";

export type WorkExperience = {
    role: string;
    company: string;
    years: number;
};

export type EventAttended = {
    event_id: string;
    name: string;
    date: string; // ISO date YYYY-MM-DD
};

export type Project = {
    name: string;
    tech: string[];
    description: string;
};

export type UserProfile = {
    // Basic (from onboarding)
    uid: string;
    name: string;
    email: string;
    phone: string;
    university?: string;
    course?: string;
    username?: string;
    googleConnected?: boolean;

    // Extended (from profile page)
    skills: string[];
    work_experience: WorkExperience[];
    events_attended: EventAttended[];
    projects: Project[];
    interests: string[];
    experience_level: "beginner" | "intermediate" | "advanced";
    preferred_domains: string[];
    location?: string;
};

export function useProfile() {
    const { user, loading: authLoading } = useAuthUser();
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user?.uid) {
            setLoading(false);
            return;
        }

        const unsubscribe = onSnapshot(doc(db, "users", user.uid), (snap) => {
            if (snap.exists()) {
                setProfile({
                    uid: user.uid,
                    ...snap.data(),
                    // Default empty arrays if not set
                    skills: snap.data().skills || [],
                    work_experience: snap.data().work_experience || [],
                    events_attended: snap.data().events_attended || [],
                    projects: snap.data().projects || [],
                    interests: snap.data().interests || [],
                    preferred_domains: snap.data().preferred_domains || [],
                    experience_level: snap.data().experience_level || "beginner",
                } as UserProfile);
            } else {
                setProfile(null);
            }
            setLoading(false);
        });

        return () => unsubscribe();
    }, [user?.uid]);

    return { profile, loading: authLoading || loading, signedIn: !!user };
}
