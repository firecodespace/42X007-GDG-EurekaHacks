export type OnboardingStepId =
    | "name"
    | "email"
    | "phone"
    | "university"
    | "course"
    | "username"
    | "google"
    | "review";

export type OnboardingDraft = {
    name: string;
    phone: string;
    email: string;

    university: string;
    course: string;

    username: string;

    googleConnected: boolean;
};
