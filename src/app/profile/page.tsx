// src/app/profile/page.tsx
"use client";

import { useState } from "react";
import { useProfile } from "@/lib/profile/useProfile";
import SkillsSection from "./_components/SkillsSection";
import ExperienceSection from "./_components/ExperienceSection";
import ProjectsSection from "./_components/ProjectsSection";
import InterestsSection from "./_components/InterestsSection";
import BasicInfoSection from "./_components/BasicInfoSection";

type Tab = "account" | "skills" | "experience" | "projects" | "interests";

export default function ProfilePage() {
    const { profile, loading } = useProfile();
    const [activeTab, setActiveTab] = useState<Tab>("account");

    if (loading) {
        return (
            <div className="flex items-center justify-center py-20">
                <div className="text-white/60">Loading profile...</div>
            </div>
        );
    }

    if (!profile) {
        return (
            <div className="flex items-center justify-center py-20 text-white/60">
                Profile not found. Complete onboarding first.
            </div>
        );
    }

    const tabs: { id: Tab; label: string }[] = [
        { id: "account", label: "Account" },
        { id: "skills", label: "Skills" },
        { id: "experience", label: "Experience" },
        { id: "projects", label: "Projects" },
        { id: "interests", label: "Interests" },
    ];

    return (
        <div>
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl sm:text-4xl lg:text-5xl font-semibold tracking-tight">
                    Profile
                </h1>
                <p className="mt-2 text-base sm:text-lg text-white/70">
                    Manage your profile and showcase your skills
                </p>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 border-b border-white/10 mb-8 overflow-x-auto">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-6 py-3 text-sm font-medium transition-colors whitespace-nowrap ${activeTab === tab.id
                                ? "text-white border-b-2 border-white"
                                : "text-white/60 hover:text-white/80"
                            }`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Tab Content */}
            <div>
                {activeTab === "account" && <BasicInfoSection profile={profile} />}
                {activeTab === "skills" && <SkillsSection profile={profile} />}
                {activeTab === "experience" && <ExperienceSection profile={profile} />}
                {activeTab === "projects" && <ProjectsSection profile={profile} />}
                {activeTab === "interests" && <InterestsSection profile={profile} />}
            </div>
        </div>
    );
}
