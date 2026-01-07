// src/app/profile/_components/ExperienceSection.tsx
"use client";

import { useState } from "react";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { UserProfile, WorkExperience } from "@/lib/profile/useProfile";
import { updateProfileField } from "@/lib/profile/updateProfile";

type Props = {
    profile: UserProfile;
};

export default function ExperienceSection({ profile }: Props) {
    const [experiences, setExperiences] = useState<WorkExperience[]>(profile.work_experience);
    const [showModal, setShowModal] = useState(false);
    const [editIndex, setEditIndex] = useState<number | null>(null);
    const [form, setForm] = useState<WorkExperience>({ role: "", company: "", years: 0 });
    const [saving, setSaving] = useState(false);

    const handleSave = async () => {
        if (!form.role || !form.company || form.years <= 0) return;

        let newExperiences: WorkExperience[];
        if (editIndex !== null) {
            newExperiences = [...experiences];
            newExperiences[editIndex] = form;
        } else {
            newExperiences = [...experiences, form];
        }

        setExperiences(newExperiences);
        setSaving(true);
        try {
            await updateProfileField(profile.uid, "work_experience", newExperiences);
            setShowModal(false);
            setForm({ role: "", company: "", years: 0 });
            setEditIndex(null);
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = async (index: number) => {
        const newExperiences = experiences.filter((_, i) => i !== index);
        setExperiences(newExperiences);

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "work_experience", newExperiences);
        } finally {
            setSaving(false);
        }
    };

    const handleEdit = (index: number) => {
        setForm(experiences[index]);
        setEditIndex(index);
        setShowModal(true);
    };

    return (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold">Work Experience</h2>
                <button
                    onClick={() => {
                        setForm({ role: "", company: "", years: 0 });
                        setEditIndex(null);
                        setShowModal(true);
                    }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white text-black font-medium hover:bg-white/90"
                >
                    <Plus className="h-4 w-4" />
                    Add Experience
                </button>
            </div>

            {/* Experience List */}
            <div className="space-y-4">
                {experiences.map((exp, i) => (
                    <div
                        key={i}
                        className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-start justify-between"
                    >
                        <div>
                            <h3 className="font-semibold text-white">{exp.role}</h3>
                            <p className="text-white/70">{exp.company}</p>
                            <p className="text-sm text-white/50 mt-1">{exp.years} years</p>
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={() => handleEdit(i)}
                                disabled={saving}
                                className="p-2 rounded-lg hover:bg-white/10 text-white/70 hover:text-white disabled:opacity-50"
                            >
                                <Pencil className="h-4 w-4" />
                            </button>
                            <button
                                onClick={() => handleDelete(i)}
                                disabled={saving}
                                className="p-2 rounded-lg hover:bg-red-500/20 text-red-400 hover:text-red-300 disabled:opacity-50"
                            >
                                <Trash2 className="h-4 w-4" />
                            </button>
                        </div>
                    </div>
                ))}
                {experiences.length === 0 && (
                    <p className="text-white/40 text-center py-8">No work experience added yet</p>
                )}
            </div>

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
                    <div className="bg-[#1a1a2e] rounded-2xl border border-white/10 p-6 w-full max-w-md">
                        <h3 className="text-xl font-semibold mb-4">
                            {editIndex !== null ? "Edit" : "Add"} Experience
                        </h3>

                        <div className="space-y-4">
                            <input
                                type="text"
                                placeholder="Role (e.g. Software Engineer)"
                                value={form.role}
                                onChange={(e) => setForm({ ...form, role: e.target.value })}
                                className="w-full h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                            />
                            <input
                                type="text"
                                placeholder="Company (e.g. Google)"
                                value={form.company}
                                onChange={(e) => setForm({ ...form, company: e.target.value })}
                                className="w-full h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                            />
                            <input
                                type="number"
                                placeholder="Years of experience"
                                value={form.years || ""}
                                onChange={(e) => setForm({ ...form, years: parseInt(e.target.value) || 0 })}
                                className="w-full h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                            />
                        </div>

                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={() => {
                                    setShowModal(false);
                                    setForm({ role: "", company: "", years: 0 });
                                    setEditIndex(null);
                                }}
                                disabled={saving}
                                className="flex-1 h-12 rounded-xl border border-white/20 text-white hover:bg-white/10 disabled:opacity-50"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleSave}
                                disabled={saving || !form.role || !form.company || form.years <= 0}
                                className="flex-1 h-12 rounded-xl bg-white text-black font-medium disabled:opacity-50"
                            >
                                {saving ? "Saving..." : "Save"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
