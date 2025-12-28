import { create } from "zustand";

type Dir = 1 | -1;

type NavDirState = {
    dir: Dir;
    forward: () => void;
    back: () => void;
};

export const useNavDirection = create<NavDirState>((set) => ({
    dir: 1,
    forward: () => set({ dir: 1 }),
    back: () => set({ dir: -1 }),
}));
