/** @odoo-module **/
/**
 * Ads On Marketing — Agency Tracker JS
 * Minimal client-side enhancements for the Odoo Kanban board.
 * Uses Odoo's OWL component framework (Odoo 16+).
 */

import { patch } from "@web/core/utils/patch";
import { KanbanRecord } from "@web/views/kanban/kanban_record";

/**
 * Patch Kanban record to add a subtle colour-coded left border
 * based on the task priority field.
 */
patch(KanbanRecord.prototype, {
    /**
     * Return extra CSS classes for the card based on priority.
     * Called by the kanban-box template.
     */
    getPriorityClass(priority) {
        const map = {
            urgent: "agency-urgent",
            high:   "agency-high",
            medium: "agency-medium",
            low:    "agency-low",
        };
        return map[priority] || "";
    },
});

// Add dynamic glow to "Stuck" Kanban column header
document.addEventListener("DOMContentLoaded", () => {
    // Runs after Odoo's UI is ready
    const observer = new MutationObserver(() => {
        document.querySelectorAll(".o_kanban_group").forEach((col) => {
            const title = col.querySelector(".o_column_title")?.textContent?.trim();
            if (title === "Stuck") {
                col.style.borderTop = "3px solid #ef4444";
            } else if (title === "Done") {
                col.style.borderTop = "3px solid #22c55e";
            } else if (title === "In Progress") {
                col.style.borderTop = "3px solid #3b82f6";
            }
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
});
