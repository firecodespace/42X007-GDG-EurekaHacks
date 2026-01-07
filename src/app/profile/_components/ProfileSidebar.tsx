// src/app/profile/_components/ProfileSidebar.tsx
"use client";

import ProfileNavItem from "./ProfileNavItem";
import { BarChart3, Bookmark, Flag, Settings, User, Users } from "lucide-react";
import { useProfile } from "@/lib/profile/useProfile";

export default function ProfileSidebar() {
    const { profile, loading } = useProfile();

    const greetingName = !loading && profile?.name
        ? profile.name.split(" ")[0]
        : "there";

    return (
        <div className="w-full">
            {/* avatar */}
            <div className="flex items-center gap-4">
                <div className="h-20 w-20 rounded-full bg-white/10 border border-white/10 flex items-center justify-center">
                    <div className="h-10 w-10 rounded-full border border-white/30" />
                </div>

                <div className="min-w-0">
                    <div className="text-lg text-white/90 truncate">
                        Hello, {greetingName}!
                    </div>
                    <div className="text-sm text-white/60 truncate">Your profile</div>
                </div>
            </div>

            {/* nav */}
            <div className="mt-8 space-y-2">
                <ProfileNavItem href="/profile" icon={<User className="h-4 w-4" />} label="Account" />
                <ProfileNavItem href="/profile/following" icon={<Users className="h-4 w-4" />} label="Following" />
                <ProfileNavItem href="/profile/milestones" icon={<Flag className="h-4 w-4" />} label="Milestones" />
                <ProfileNavItem href="/profile/preferences" icon={<Settings className="h-4 w-4" />} label="Preferences" />
                <ProfileNavItem href="/profile/sources" icon={<Bookmark className="h-4 w-4" />} label="Sources" />
                <ProfileNavItem href="/profile/insights" icon={<BarChart3 className="h-4 w-4" />} label="Insights" />
            </div>
        </div>
    );
}
