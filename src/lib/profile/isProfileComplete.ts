import type { UserProfile } from "./profileStore";

export function isProfileComplete(p: UserProfile) {
    return Boolean(
        p.name?.trim() &&
        p.email?.trim() &&
        p.phone?.trim() &&
        p.university?.trim() &&
        p.course?.trim() &&
        p.username?.trim()
    );
}
