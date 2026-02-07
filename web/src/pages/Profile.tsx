import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { Camera, RefreshCw, User, Palette, Droplets } from "lucide-react";
import { getUserProfile, uploadPhoto } from "@/lib/api";
import FileUpload from "@/components/FileUpload";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

const toneColors: Record<string, string> = {
  FAIR: "bg-amber-100 text-amber-800 border-amber-200",
  MEDIUM: "bg-amber-300 text-amber-900 border-amber-400",
  DARK: "bg-amber-700 text-amber-50 border-amber-800",
};

const undertoneColors: Record<string, string> = {
  WARM: "bg-orange-100 text-orange-800 border-orange-200",
  COOL: "bg-blue-100 text-blue-800 border-blue-200",
  NEUTRAL: "bg-secondary text-secondary-foreground border-border",
};

export default function Profile() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const { data: profile, isLoading, isError } = useQuery({
    queryKey: ["profile"],
    queryFn: getUserProfile,
    retry: false,
  });

  const mutation = useMutation({
    mutationFn: (file: File) => uploadPhoto(file),
    onSuccess: () => {
      toast({ title: "Photo analyzed!", description: "Your skin tone has been detected." });
      queryClient.invalidateQueries({ queryKey: ["profile"] });
      setSelectedFile(null);
    },
    onError: (err: Error) => {
      toast({ title: "Upload failed", description: err.message, variant: "destructive" });
    },
  });

  const hasProfile = profile?.skin_tone;

  return (
    <div className="mx-auto max-w-2xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-foreground">My Profile</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Upload a face photo so our AI can analyze your skin tone
        </p>
      </div>

      {hasProfile ? (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Photo + Info */}
          <div className="flex flex-col items-center gap-6 rounded-2xl bg-card p-8 shadow-card sm:flex-row sm:items-start">
            <div className="relative">
              <img
                src={profile.photo_url}
                alt="Your face"
                className="h-36 w-36 rounded-2xl object-cover shadow-md"
              />
              <div className="absolute -bottom-2 -right-2 flex h-8 w-8 items-center justify-center rounded-full bg-success text-success-foreground shadow-md">
                <User className="h-4 w-4" />
              </div>
            </div>

            <div className="flex-1 space-y-4 text-center sm:text-left">
              <h2 className="text-lg font-semibold text-foreground">
                Analysis Complete
              </h2>

              <div className="flex flex-wrap justify-center gap-3 sm:justify-start">
                <div className="flex items-center gap-2">
                  <Palette className="h-4 w-4 text-muted-foreground" />
                  <span
                    className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold ${
                      toneColors[profile.skin_tone] || toneColors.MEDIUM
                    }`}
                  >
                    {profile.skin_tone}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Droplets className="h-4 w-4 text-muted-foreground" />
                  <span
                    className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold ${
                      undertoneColors[profile.skin_undertone] || undertoneColors.NEUTRAL
                    }`}
                  >
                    {profile.skin_undertone} undertone
                  </span>
                </div>
              </div>

              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedFile(null)}
                className="gap-2"
              >
                <RefreshCw className="h-3.5 w-3.5" />
                Re-analyze
              </Button>
            </div>
          </div>

          {/* Re-upload area */}
          <div className="space-y-3">
            <p className="text-sm font-medium text-foreground">Upload a new photo</p>
            <FileUpload onFileSelect={setSelectedFile} accept="image/*" compact />
            {selectedFile && (
              <Button
                onClick={() => mutation.mutate(selectedFile)}
                disabled={mutation.isPending}
                className="w-full gap-2 gradient-primary text-primary-foreground"
              >
                {mutation.isPending ? (
                  <RefreshCw className="h-4 w-4 animate-spin" />
                ) : (
                  <Camera className="h-4 w-4" />
                )}
                {mutation.isPending ? "Analyzing..." : "Analyze Photo"}
              </Button>
            )}
          </div>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <div className="rounded-2xl bg-card p-8 shadow-card">
            <FileUpload
              onFileSelect={setSelectedFile}
              accept="image/*"
              label="Upload your face photo"
              sublabel="We'll analyze your skin tone and undertone using AI"
            />
          </div>

          {selectedFile && (
            <Button
              onClick={() => mutation.mutate(selectedFile)}
              disabled={mutation.isPending}
              className="w-full gap-2 gradient-primary text-primary-foreground"
              size="lg"
            >
              {mutation.isPending ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <Camera className="h-4 w-4" />
              )}
              {mutation.isPending ? "Analyzing your photo..." : "Analyze My Skin Tone"}
            </Button>
          )}

          {isLoading && (
            <div className="flex justify-center py-8">
              <RefreshCw className="h-6 w-6 animate-spin text-primary" />
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}
