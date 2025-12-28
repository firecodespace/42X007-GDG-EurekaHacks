"use client";

import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

export type OnboardingDraft = {
    name: string;
    email: string;
    phone: string;
    university: string;
    course: string;
    username: string;
    googleConnected: boolean;
};

const STORAGE_KEY = "hackflix:onboarding:v1";

const initialDraft: OnboardingDraft = {
    name: "",
    email: "",
    phone: "",
    university: "",
    course: "",
    username: "",
    googleConnected: false,
};

type Ctx = {
    draft: OnboardingDraft;
    setDraft: React.Dispatch<React.SetStateAction<OnboardingDraft>>;
    reset: () => void;
};

const OnboardingContext = createContext<Ctx | null>(null);

export function OnboardingProvider({ children }: { children: React.ReactNode }) {
    const [draft, setDraft] = useState<OnboardingDraft>(initialDraft);

    useEffect(() => {
        try {
            const raw = sessionStorage.getItem(STORAGE_KEY);
            if (!raw) return;
            const parsed = JSON.parse(raw) as Partial<OnboardingDraft>;
            setDraft((p) => ({ ...p, ...parsed }));
        } catch {
            return;
        }
    }, []);

    useEffect(() => {
        try {
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(draft));
        } catch {
            return;
        }
    }, [draft]);

    const value = useMemo(
        () => ({
            draft,
            setDraft,
            reset: () => {
                setDraft(initialDraft);
                try {
                    sessionStorage.removeItem(STORAGE_KEY);
                } catch {
                    return;
                }
            },
        }),
        [draft]
    );

    return <OnboardingContext.Provider value={value}>{children}</OnboardingContext.Provider>;
}

export function useOnboarding() {
    const ctx = useContext(OnboardingContext);
    if (!ctx) throw new Error("useOnboarding must be used inside OnboardingProvider");
    return ctx;
}
