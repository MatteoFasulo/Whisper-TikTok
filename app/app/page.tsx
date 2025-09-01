"use client"
import { SidebarDemo } from "@/components/home/SidebarComponent";
import { Hero } from "@/components/ui/animated-hero";

export default function Home() {
  return (
    <div className="flex min-h-screen">
      <SidebarDemo />
      <main className="flex flex-1 items-center justify-center bg-white dark:bg-neutral-900">
        <Hero />
      </main>
    </div>
  );
}