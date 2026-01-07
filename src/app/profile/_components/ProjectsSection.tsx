// src/app/profile/_components/ProjectsSection.tsx
"use client";

import { useState } from "react";
import { Plus, Pencil, Trash2, X } from "lucide-react";
import { UserProfile, Project } from "@/lib/profile/useProfile";
import { updateProfileField } from "@/lib/profile/updateProfile";

type Props = {
    profile: UserProfile;
};

export default function ProjectsSection({ profile }: Props) {
    const [projects, setProjects] = useState<Project[]>(profile.projects);
    const [showModal, setShowModal] = useState(false);
    const [editIndex, setEditIndex] = useState<number | null>(null);
    const [form, setForm] = useState<Project>({ name: "", tech: [], description: "" });
    const [techInput, setTechInput] = useState("");
    const [saving, setSaving] = useState(false);

    const handleSave = async () => {
        if (!form.name || !form.description || form.tech.length === 0) return;

        let newProjects: Project[];
        if (editIndex !== null) {
            newProjects = [...projects];
            newProjects[editIndex] = form;
        } else {
            newProjects = [...projects, form];
        }

        setProjects(newProjects);
        setSaving(true);
        try {
            await updateProfileField(profile.uid, "projects", newProjects);
            setShowModal(false);
            setForm({ name: "", tech: [], description: "" });
            setEditIndex(null);
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = async (index: number) => {
        const newProjects = projects.filter((_, i) => i !== index);
        setProjects(newProjects);

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "projects", newProjects);
        } finally {
            setSaving(false);
        }
    };

    const handleEdit = (index: number) => {
        setForm(projects[index]);
        setEditIndex(index);
        setShowModal(true);
    };

    const addTech = () => {
        if (!techInput.trim()) return;
        setForm({ ...form, tech: [...form.tech, techInput.trim()] });
        setTechInput("");
    };

    const removeTech = (index: number) => {
        setForm({ ...form, tech: form.tech.filter((_, i) => i !== index) });
    };

    return (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold">Projects</h2>
                <button
                    onClick={() => {
                        setForm({ name: "", tech: [], description: "" });
                        setEditIndex(null);
                        setShowModal(true);
                    }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white text-black font-medium hover:bg-white/90"
                >
                    <Plus className="h-4 w-4" />
                    Add Project
                </button>
            </div>

            {/* Projects List */}
            <div className="space-y-4">
                {projects.map((project, i) => (
                    <div
                        key={i}
                        className="p-4 rounded-xl bg-white/5 border border-white/10"
                    >
                        <div className="flex items-start justify-between mb-2">
                            <h3 className="font-semibold text-white">{project.name}</h3>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => handleEdit(i)}
                                    disabled={saving}
                                    className="p-2 rounded-lg hover:bg-white/10 text-white/70 hover:text-white"
                                >
                                    <Pencil className="h-4 w-4" />
                                </button>
                                <button
                                    onClick={() => handleDelete(i)}
                                    disabled={saving}
                                    className="p-2 rounded-lg hover:bg-red-500/20 text-red-400 hover:text-red-300"
                                >
                                    <Trash2 className="h-4 w-4" />
                                </button>
                            </div>
                        </div>
                        <p className="text-white/70 text-sm mb-3">{project.description}</p>
                        <div className="flex flex-wrap gap-2">
                            {project.tech.map((t, idx) => (
                                <span
                                    key={idx}
                                    className="px-3 py-1 rounded-full bg-white/10 text-xs text-white/80"
                                >
                                    {t}
                                </span>
                            ))}
                        </div>
                    </div>
                ))}
                {projects.length === 0 && (
                    <p className="text-white/40 text-center py-8">No projects added yet</p>
                )}
            </div>

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
                    <div className="bg-[#1a1a2e] rounded-2xl border border-white/10 p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
                        <h3 className="text-xl font-semibold mb-4">
                            {editIndex !== null ? "Edit" : "Add"} Project
                        </h3>

                        <div className="space-y-4">
                            <input
                                type="text"
                                placeholder="Project name"
                                value={form.name}
                                onChange={(e) => setForm({ ...form, name: e.target.value })}
                                className="w-full h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                            />

                            <textarea
                                placeholder="Description"
                                value={form.description}
                                onChange={(e) => setForm({ ...form, description: e.target.value })}
                                rows={3}
                                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30 resize-none"
                            />

                            {/* Tech Stack */}
                            <div>
                                <label className="text-sm text-white/70 mb-2 block">Tech Stack</label>
                                <div className="flex gap-2 mb-3">
                                    <input
                                        type="text"
                                        placeholder="Add technology"
                                        value={techInput}
                                        onChange={(e) => setTechInput(e.target.value)}
                                        onKeyDown={(e) => e.key === "Enter" && addTech()}
                                        className="flex-1 h-10 px-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30 text-sm"
                                    />
                                    <button
                                        onClick={addTech}
                                        className="px-4 h-10 rounded-lg bg-white/10 text-white text-sm hover:bg-white/20"
                                    >
                                        Add
                                    </button>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                    {form.tech.map((t, idx) => (
                                        <div
                                            key={idx}
                                            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-sm"
                                        >
                                            <span>{t}</span>
                                            <button onClick={() => removeTech(idx)}>
                                                <X className="h-3 w-3" />
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={() => {
                                    setShowModal(false);
                                    setForm({ name: "", tech: [], description: "" });
                                    setEditIndex(null);
                                }}
                                disabled={saving}
                                className="flex-1 h-12 rounded-xl border border-white/20 text-white hover:bg-white/10"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleSave}
                                disabled={saving || !form.name || !form.description || form.tech.length === 0}
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
