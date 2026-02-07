import { Link } from "react-router-dom";
import { Shirt, User, Sparkles, Camera, Plus, ArrowRight } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { getAllClothing, getUserProfile } from "@/lib/api";
import StatCard from "@/components/StatCard";
import heroBg from "@/assets/hero-bg.jpg";

const fadeUp = {
  hidden: { opacity: 0, y: 16 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.4 },
  }),
};

export default function Dashboard() {
  const { data: clothing } = useQuery({
    queryKey: ["clothing"],
    queryFn: getAllClothing,
    retry: false,
  });

  const { data: profile } = useQuery({
    queryKey: ["profile"],
    queryFn: getUserProfile,
    retry: false,
  });

  const clothingCount = clothing?.length ?? 0;
  const skinStatus = profile?.skin_tone ? "Analyzed" : "Pending";

  return (
    <div className="space-y-8">
      {/* Hero */}
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative overflow-hidden rounded-2xl"
      >
        <img
          src={heroBg}
          alt=""
          className="absolute inset-0 h-full w-full object-cover"
        />
        <div className="absolute inset-0 gradient-hero opacity-80" />
        <div className="relative z-10 px-6 py-14 sm:px-10 sm:py-20">
          <h1 className="text-3xl font-extrabold tracking-tight text-primary-foreground sm:text-4xl lg:text-5xl">
            WhatToWear
          </h1>
          <p className="mt-3 max-w-lg text-sm text-primary-foreground/80 sm:text-base">
            AI-powered outfit suggestions based on your skin tone, weather, and
            occasion. Look your best every single day.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              to="/profile"
              className="inline-flex items-center gap-2 rounded-lg gradient-accent px-5 py-2.5 text-sm font-semibold text-accent-foreground shadow-md transition-transform hover:scale-105"
            >
              <Camera className="h-4 w-4" />
              Upload Photo
            </Link>
            <Link
              to="/wardrobe"
              className="inline-flex items-center gap-2 rounded-lg bg-primary-foreground/15 px-5 py-2.5 text-sm font-semibold text-primary-foreground backdrop-blur-sm transition-colors hover:bg-primary-foreground/25"
            >
              <Plus className="h-4 w-4" />
              Add Clothing
            </Link>
            <Link
              to="/recommendations"
              className="inline-flex items-center gap-2 rounded-lg bg-primary-foreground/15 px-5 py-2.5 text-sm font-semibold text-primary-foreground backdrop-blur-sm transition-colors hover:bg-primary-foreground/25"
            >
              <Sparkles className="h-4 w-4" />
              Get Suggestions
            </Link>
          </div>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-3">
        <motion.div variants={fadeUp} initial="hidden" animate="visible" custom={0}>
          <StatCard label="Clothing Items" value={clothingCount} icon={Shirt} />
        </motion.div>
        <motion.div variants={fadeUp} initial="hidden" animate="visible" custom={1}>
          <StatCard
            label="Skin Analysis"
            value={skinStatus}
            icon={User}
            variant={profile?.skin_tone ? "primary" : "default"}
          />
        </motion.div>
        <motion.div variants={fadeUp} initial="hidden" animate="visible" custom={2}>
          <StatCard
            label="Get Styled"
            value="Ready"
            icon={Sparkles}
            variant="accent"
          />
        </motion.div>
      </div>

      {/* Quick actions */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.35 }}
      >
        <h2 className="mb-4 text-lg font-semibold text-foreground">
          Quick Actions
        </h2>
        <div className="grid gap-3 sm:grid-cols-3">
          {[
            { to: "/profile", label: "Analyze Skin Tone", icon: Camera, desc: "Upload a face photo for AI analysis" },
            { to: "/wardrobe", label: "Manage Wardrobe", icon: Shirt, desc: "Add and organize your clothing" },
            { to: "/recommendations", label: "Get Outfit Ideas", icon: Sparkles, desc: "AI picks the best outfit for you" },
          ].map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className="group flex items-center gap-4 rounded-xl bg-card p-4 shadow-card transition-all duration-200 hover:shadow-card-hover"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                <item.icon className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-foreground">{item.label}</p>
                <p className="text-xs text-muted-foreground">{item.desc}</p>
              </div>
              <ArrowRight className="h-4 w-4 text-muted-foreground transition-transform group-hover:translate-x-1" />
            </Link>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
