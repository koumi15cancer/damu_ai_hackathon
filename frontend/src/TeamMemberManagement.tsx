import React, { useState, useEffect } from "react";
import {
  Add,
  Edit,
  Delete,
  LocationOn,
  Psychology,
} from "@mui/icons-material";
import axios from "axios";
import { Button } from "./components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "./components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./components/ui/dialog";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select";
import { Badge } from "./components/ui/badge";
import { CircularProgress } from "@mui/material";

interface TeamMember {
  id: string;
  name: string;
  location: string;
  preferences: string[];
  vibe: string;
}

interface NewTeamMember {
  name: string;
  location: string;
  preferences: string[];
  vibe: string;
}

function TeamMemberManagement() {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [editingMember, setEditingMember] = useState<TeamMember | null>(null);
  const [newMember, setNewMember] = useState<NewTeamMember>({
    name: "",
    location: "",
    preferences: [],
    vibe: "Mixed",
  });

  const vibeOptions = ["Chill", "Energetic", "Mixed"];
  const preferenceOptions = [
    "Vegetarian",
    "Meat-lover",
    "BBQ",
    "Hotpot",
    "Karaoke",
    "Bar",
    "Cafe-hopping",
    "Games",
    "Outdoor walks",
    "Movie night",
    "Rooftop bar",
    "Dinner & chat",
    "Office snacks",
    "Asian food",
  ];

  useEffect(() => {
    loadTeamMembers();
  }, []);

  const loadTeamMembers = async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://localhost:5000/team-members");
      setTeamMembers(response.data);
    } catch (error) {
      console.error("Failed to load team members:", error);
      setError(
        "Failed to load team members. Please check if the backend server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSaveMember = async () => {
    if (editingMember) {
      await handleUpdateMember();
    } else {
      await handleAddMember();
    }
  };

  const handleAddMember = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        "http://localhost:5000/team-members",
        newMember
      );
      setTeamMembers([...teamMembers, response.data]);
      setDialogOpen(false);
      resetForm();
    } catch (error) {
      console.error("Failed to add team member:", error);
      setError("Failed to add team member. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateMember = async () => {
    if (!editingMember) return;

    try {
      setLoading(true);
      const response = await axios.put(
        `http://localhost:5000/team-members/${editingMember.id}`,
        newMember
      );
      setTeamMembers(
        teamMembers.map((member) =>
          member.id === editingMember.id ? response.data : member
        )
      );
      setDialogOpen(false);
      resetForm();
    } catch (error) {
      console.error("Failed to update team member:", error);
      setError("Failed to update team member. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteMember = async (memberId: string) => {
    if (!window.confirm("Are you sure you want to delete this team member?"))
      return;

    try {
      setLoading(true);
      await axios.delete(`http://localhost:5000/team-members/${memberId}`);
      setTeamMembers(teamMembers.filter((member) => member.id !== memberId));
    } catch (error) {
      console.error("Failed to delete team member:", error);
      setError("Failed to delete team member. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const openEditDialog = (member: TeamMember) => {
    setEditingMember(member);
    setNewMember({
      name: member.name,
      location: member.location,
      preferences: member.preferences,
      vibe: member.vibe,
    });
    setDialogOpen(true);
  };

  const openAddDialog = () => {
    setEditingMember(null);
    resetForm();
    setDialogOpen(true);
  };

  const resetForm = () => {
    setEditingMember(null);
    setNewMember({ name: "", location: "", preferences: [], vibe: "Mixed" });
  };

  const handlePreferenceToggle = (preference: string) => {
    setNewMember((prev) => ({
      ...prev,
      preferences: prev.preferences.includes(preference)
        ? prev.preferences.filter((p) => p !== preference)
        : [...prev.preferences, preference],
    }));
  };

  const getVibeBadgeVariant = (
    vibe: string
  ): "default" | "secondary" | "destructive" | "outline" => {
    switch (vibe) {
      case "Chill":
        return "default";
      case "Energetic":
        return "destructive";
      case "Mixed":
        return "secondary";
      default:
        return "outline";
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-foreground">
          Team Member Management
        </h1>
        <Button onClick={openAddDialog}>
          <Add className="mr-2 h-4 w-4" /> Add Member
        </Button>
      </div>

      {error && (
        <div className="bg-destructive/10 border border-destructive/20 text-destructive p-4 rounded-md">
          <h5 className="font-bold">Error</h5>
          <p>{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {teamMembers.map((member) => (
          <Card key={member.id} className="flex flex-col">
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle>{member.name}</CardTitle>
                <div className="flex space-x-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => openEditDialog(member)}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDeleteMember(member.id)}
                  >
                    <Delete className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="flex-grow space-y-3">
              <div className="flex items-center text-sm text-muted-foreground">
                <LocationOn className="h-4 w-4 mr-2" />
                {member.location}
              </div>
              <div className="flex items-center text-sm">
                <Psychology className="h-4 w-4 mr-2 text-muted-foreground" />
                <Badge variant={getVibeBadgeVariant(member.vibe)}>
                  {member.vibe}
                </Badge>
              </div>
              <div>
                <h4 className="font-semibold text-sm mb-2">Preferences</h4>
                <div className="flex flex-wrap gap-2">
                  {member.preferences.map((pref, index) => (
                    <Badge key={index} variant="outline">
                      {pref}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editingMember ? "Edit Team Member" : "Add New Team Member"}
            </DialogTitle>
          </DialogHeader>
          <div className="py-4 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={newMember.name}
                onChange={(e) =>
                  setNewMember({ ...newMember, name: e.target.value })
                }
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>
              <Input
                id="location"
                value={newMember.location}
                onChange={(e) =>
                  setNewMember({ ...newMember, location: e.target.value })
                }
              />
            </div>
            <div className="space-y-2">
              <Label>Vibe</Label>
              <Select
                value={newMember.vibe}
                onValueChange={(value) =>
                  setNewMember({ ...newMember, vibe: value })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a vibe" />
                </SelectTrigger>
                <SelectContent>
                  {vibeOptions.map((vibe) => (
                    <SelectItem key={vibe} value={vibe}>
                      {vibe}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Preferences</Label>
              <div className="flex flex-wrap gap-2 p-2 border rounded-md min-h-[40px]">
                {preferenceOptions.map((pref) => (
                  <Button
                    key={pref}
                    variant={
                      newMember.preferences.includes(pref)
                        ? "default"
                        : "outline"
                    }
                    size="sm"
                    onClick={() => handlePreferenceToggle(pref)}
                    className="h-auto py-1 px-2 text-xs"
                  >
                    {pref}
                  </Button>
                ))}
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleSaveMember} disabled={loading}>
              {loading && <CircularProgress size={20} className="mr-2" />}
              {editingMember ? "Save Changes" : "Add Member"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default TeamMemberManagement;
