// src/app/profile/_components/BasicInfoSection.tsx
"use client";

import { useState } from "react";
import { UserProfile } from "@/lib/profile/useProfile";
import { updateProfileField } from "@/lib/profile/updateProfile";

type Props = {
    profile: UserProfile;
};

export default function BasicInfoSection({ profile }: Props) {
    const [experienceLevel, setExperienceLevel] = useState(profile.experience_level);
    const [location, setLocation] = useState(profile.location || "");
    const [saving, setSaving] = useState(false);

    const handleSaveExperienceLevel = async (level: "beginner" | "intermediate" | "advanced") => {
        setSaving(true);
        setExperienceLevel(level);
        try {
            await updateProfileField(profile.uid, "experience_level", level);
        } catch (e) {
            console.error(e);
        } finally {
            setSaving(false);
        }
    };

    const handleSaveLocation = async () => {
        setSaving(true);
        try {
            await updateProfileField(profile.uid, "location", location);
        } catch (e) {
            console.error(e);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="space-y-6">
            {/* Basic Info (read-only) */}
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <h2 className="text-xl font-semibold mb-4">Basic Information</h2>
                <div className="space-y-3">
                    <Row label="Name" value={profile.name} />
                    <Row label="Email" value={profile.email} />
                    <Row label="Phone" value={profile.phone} />
                    <Row label="University" value={profile.university || "—"} />
                    <Row label="Course" value={profile.course || "—"} />
                    <Row label="Username" value={profile.username || "—"} />
                </div>
            </div>

            {/* Experience Level */}
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <h2 className="text-xl font-semibold mb-4">Experience Level</h2>
                <div className="flex gap-3">
                    {(["beginner", "intermediate", "advanced"] as const).map((level) => (
                        <button
                            key={level}
                            disabled={saving}
                            onClick={() => handleSaveExperienceLevel(level)}
                            className={`px-6 py-2 rounded-xl font-medium transition-all ${experienceLevel === level
                                    ? "bg-white text-black"
                                    : "bg-white/10 text-white/70 hover:bg-white/20"
                                } disabled:opacity-50`}
                        >
                            {level.charAt(0).toUpperCase() + level.slice(1)}
                        </button>
                    ))}
                </div>
            </div>

            {/* Location */}
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <h2 className="text-xl font-semibold mb-4">Location</h2>
                <div className="flex gap-3">
                    <input
                        type="text"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        placeholder="e.g. Mumbai, India"
                        className="flex-1 h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                    />
                    <button
                        onClick={handleSaveLocation}
                        disabled={saving || location === profile.location}
                        className="px-6 h-12 rounded-xl bg-white text-black font-medium disabled:opacity-50"
                    >
                        {saving ? "Saving..." : "Save"}
                    </button>
                </div>
            </div>
        </div>
    );
}

function Row({ label, value }: { label: string; value: string }) {
    return (
        <div className="flex items-center justify-between py-2">
            <span className="text-white/60">{label}</span>
            <span className="text-white font-medium">{value}</span>
        </div>
    );
}
