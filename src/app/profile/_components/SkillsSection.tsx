// src/app/profile/_components/SkillsSection.tsx
"use client";

import { useState } from "react";
import { X } from "lucide-react";
import { UserProfile } from "@/lib/profile/useProfile";
import { updateProfileField } from "@/lib/profile/updateProfile";

type Props = {
    profile: UserProfile;
};

export default function SkillsSection({ profile }: Props) {
    const [skills, setSkills] = useState<string[]>(profile.skills);
    const [input, setInput] = useState("");
    const [saving, setSaving] = useState(false);

    const handleAdd = async () => {
        if (!input.trim()) return;
        const newSkills = [...skills, input.trim()];
        setSkills(newSkills);
        setInput("");

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "skills", newSkills);
        } catch (e) {
            console.error(e);
            setSkills(skills); // Rollback
        } finally {
            setSaving(false);
        }
    };

    const handleRemove = async (index: number) => {
        const newSkills = skills.filter((_, i) => i !== index);
        setSkills(newSkills);

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "skills", newSkills);
        } catch (e) {
            console.error(e);
            setSkills(skills); // Rollback
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-xl font-semibold mb-4">Skills</h2>

            {/* Add Skill */}
            <div className="flex gap-3 mb-6">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleAdd()}
                    placeholder="Add a skill (e.g. Java, Python)"
                    className="flex-1 h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                    disabled={saving}
                />
                <button
                    onClick={handleAdd}
                    disabled={saving || !input.trim()}
                    className="px-6 h-12 rounded-xl bg-white text-black font-medium disabled:opacity-50"
                >
                    Add
                </button>
            </div>

            {/* Skills Chips */}
            <div className="flex flex-wrap gap-2">
                {skills.map((skill, i) => (
                    <div
                        key={i}
                        className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20 text-white"
                    >
                        <span>{skill}</span>
                        <button
                            onClick={() => handleRemove(i)}
                            disabled={saving}
                            className="hover:bg-white/20 rounded-full p-0.5 disabled:opacity-50"
                        >
                            <X className="h-4 w-4" />
                        </button>
                    </div>
                ))}
                {skills.length === 0 && (
                    <p className="text-white/40 text-sm">No skills added yet</p>
                )}
            </div>
        </div>
    );
}
