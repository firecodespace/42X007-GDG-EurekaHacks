"use client";

import { useRouter } from "next/navigation";
import { ArrowLeft, ArrowRight } from "lucide-react";
import AutocompleteInput from "@/components/ui/AutocompleteInput";
import { UNIVERSITY_OPTIONS } from "@/mocks/universities";
import { useOnboarding } from "@/lib/onboarding/store";

export default function OnboardingUniversityPage() {
    const router = useRouter();
    const { draft, setDraft } = useOnboarding();

    const canContinue = draft.university.trim().length >= 2;

    return (
        <main className="min-h-dvh px-5 sm:px-8 lg:px-10 py-10 sm:py-14 lg:py-16 text-white">
            <div className="max-w-5xl">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight">
                    University
                </h1>
                <p className="mt-3 sm:mt-4 text-lg sm:text-xl lg:text-2xl text-white/70">
                    Type to search and select.
                </p>

                <div className="mt-10 sm:mt-14">
                    <div className="flex items-end gap-4 sm:gap-6">
                        <div className="flex-1">
                            <AutocompleteInput
                                label="University"
                                placeholder="Start typing..."
                                value={draft.university}
                                onChange={(v) => setDraft((p) => ({ ...p, university: v }))}
                                options={UNIVERSITY_OPTIONS}
                                showUnderline={false}
                            />
                        </div>

                        <div className="flex items-center gap-4 sm:gap-5 pb-2">
                            <button
                                type="button"
                                aria-label="Back"
                                onClick={() => router.back()}
                                className="cursor-pointer p-3 sm:p-2 text-white/80 hover:text-white"
                            >
                                <ArrowLeft className="h-6 w-6 sm:h-7 sm:w-7" />
                            </button>

                            <button
                                type="button"
                                aria-label="Continue"
                                onClick={() => router.push("/onboarding/course")}
                                disabled={!canContinue}
                                className="cursor-pointer p-3 sm:p-2 text-white/90 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
                            >
                                <ArrowRight className="h-6 w-6 sm:h-7 sm:w-7" />
                            </button>
                        </div>
                    </div>

                    <div className="mt-5 sm:mt-6 h-px w-full bg-white/30" />
                </div>
            </div>
        </main>
    );
}
