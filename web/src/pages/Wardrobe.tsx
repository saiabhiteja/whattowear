import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, Shirt, X, RefreshCw, Filter } from "lucide-react";
import {
  getAllClothing,
  uploadClothing,
  imageUrl,
  CLOTHING_TYPES,
  OCCASIONS,
  SEASONS,
  type ClothingItem,
} from "@/lib/api";
import FileUpload from "@/components/FileUpload";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";

function ClothingCard({ item }: { item: ClothingItem }) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="group overflow-hidden rounded-xl bg-card shadow-card transition-all duration-200 hover:shadow-card-hover"
    >
      <div className="relative aspect-square overflow-hidden">
        <img
          src={imageUrl(item.image_url)}
          alt={item.clothing_type}
          className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
        />
      </div>
      <div className="p-3 space-y-2">
        <div className="flex items-center gap-2">
          <div
            className="h-4 w-4 rounded-full border border-border shadow-sm"
            style={{ backgroundColor: item.dominant_color }}
            title={`Dominant: ${item.dominant_color}`}
          />
          {item.secondary_color && (
            <div
              className="h-3 w-3 rounded-full border border-border"
              style={{ backgroundColor: item.secondary_color }}
              title={`Secondary: ${item.secondary_color}`}
            />
          )}
        </div>
        <div className="flex flex-wrap gap-1.5">
          <span className="rounded-md bg-primary/10 px-2 py-0.5 text-[10px] font-semibold text-primary">
            {item.clothing_type}
          </span>
          <span className="rounded-md bg-secondary px-2 py-0.5 text-[10px] font-medium text-secondary-foreground">
            {item.occasion}
          </span>
          <span className="rounded-md bg-muted px-2 py-0.5 text-[10px] font-medium text-muted-foreground">
            {item.season}
          </span>
        </div>
      </div>
    </motion.div>
  );
}

export default function Wardrobe() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [clothingType, setClothingType] = useState("");
  const [occasion, setOccasion] = useState("");
  const [season, setSeason] = useState("");
  const [filterType, setFilterType] = useState<string>("ALL");

  const { data: clothing, isLoading } = useQuery({
    queryKey: ["clothing"],
    queryFn: getAllClothing,
    retry: false,
  });

  const mutation = useMutation({
    mutationFn: () => uploadClothing(selectedFile!, clothingType, occasion, season),
    onSuccess: () => {
      toast({ title: "Clothing added!", description: "Your wardrobe has been updated." });
      queryClient.invalidateQueries({ queryKey: ["clothing"] });
      resetForm();
    },
    onError: (err: Error) => {
      toast({ title: "Upload failed", description: err.message, variant: "destructive" });
    },
  });

  const resetForm = () => {
    setOpen(false);
    setSelectedFile(null);
    setClothingType("");
    setOccasion("");
    setSeason("");
  };

  const canSubmit = selectedFile && clothingType && occasion && season;

  const filteredClothing =
    filterType === "ALL"
      ? clothing
      : clothing?.filter((item) => item.clothing_type === filterType);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">My Wardrobe</h1>
          <p className="text-sm text-muted-foreground">
            {clothing?.length ?? 0} items in your collection
          </p>
        </div>
        <Button onClick={() => setOpen(true)} className="gap-2 gradient-primary text-primary-foreground">
          <Plus className="h-4 w-4" />
          Add Clothing
        </Button>
      </div>

      {/* Filter */}
      {clothing && clothing.length > 0 && (
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-muted-foreground" />
          <Select value={filterType} onValueChange={setFilterType}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Filter by type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ALL">All Types</SelectItem>
              {CLOTHING_TYPES.map((t) => (
                <SelectItem key={t} value={t}>
                  {t}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      )}

      {/* Grid */}
      {isLoading ? (
        <div className="flex justify-center py-16">
          <RefreshCw className="h-6 w-6 animate-spin text-primary" />
        </div>
      ) : filteredClothing && filteredClothing.length > 0 ? (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <AnimatePresence>
            {filteredClothing.map((item) => (
              <ClothingCard key={item.id} item={item} />
            ))}
          </AnimatePresence>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center rounded-2xl bg-card py-20 shadow-card"
        >
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
            <Shirt className="h-8 w-8 text-primary" />
          </div>
          <h3 className="mt-4 text-lg font-semibold text-foreground">
            Your wardrobe is empty
          </h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Start by adding some clothes!
          </p>
          <Button
            onClick={() => setOpen(true)}
            className="mt-5 gap-2 gradient-primary text-primary-foreground"
          >
            <Plus className="h-4 w-4" />
            Add Your First Item
          </Button>
        </motion.div>
      )}

      {/* Upload Dialog */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Add Clothing Item</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <FileUpload
              onFileSelect={setSelectedFile}
              accept="image/*"
              compact
              label="Drop clothing image"
              sublabel="PNG, JPG"
            />
            <Select value={clothingType} onValueChange={setClothingType}>
              <SelectTrigger>
                <SelectValue placeholder="Clothing Type" />
              </SelectTrigger>
              <SelectContent>
                {CLOTHING_TYPES.map((t) => (
                  <SelectItem key={t} value={t}>
                    {t}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={occasion} onValueChange={setOccasion}>
              <SelectTrigger>
                <SelectValue placeholder="Occasion" />
              </SelectTrigger>
              <SelectContent>
                {OCCASIONS.map((o) => (
                  <SelectItem key={o} value={o}>
                    {o}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={season} onValueChange={setSeason}>
              <SelectTrigger>
                <SelectValue placeholder="Season" />
              </SelectTrigger>
              <SelectContent>
                {SEASONS.map((s) => (
                  <SelectItem key={s} value={s}>
                    {s}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button
              onClick={() => mutation.mutate()}
              disabled={!canSubmit || mutation.isPending}
              className="w-full gap-2 gradient-primary text-primary-foreground"
            >
              {mutation.isPending ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <Plus className="h-4 w-4" />
              )}
              {mutation.isPending ? "Uploading..." : "Add to Wardrobe"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
