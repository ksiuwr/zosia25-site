import { AdminCenteredContentContainer } from "@client/components/admin/layout/AdminCenteredContentContainer";
import { AdminLayout } from "@client/components/admin/layout/AdminLayout";
import { AdminSponsorsActiveCheckbox } from "@client/components/admin/sponsors/AdminSponsorsActiveCheckbox";
import { AdminTable } from "@client/components/admin/tables/AdminTable";
import { AdminTableActions } from "@client/components/admin/tables/AdminTableActions";
import { AdminTableEditLink } from "@client/components/admin/tables/AdminTableEditLink";
import { PageTitle } from "@client/components/PageTitle";
import { reverse, templates } from "@reactivated";
import clsx from "clsx";
import React from "react";

export const Template = (props: templates.AdminSponsorsList) => {
  return (
    <AdminLayout>
      <PageTitle>Sponsors</PageTitle>
      <AdminCenteredContentContainer>
        <AdminTable headerNames={["Name", "Type", "Active", "Actions"]}>
          {props.sponsors
            .sort((sponsor1, sponsor2) =>
              sponsor1.name.localeCompare(sponsor2.name),
            )
            .map((sponsor) => (
              <tr key={sponsor.id}>
                <td>{sponsor.name}</td>
                <td>
                  <span
                    className={clsx(
                      "badge lg:badge-lg",
                      sponsor.sponsor_type === "gold" &&
                        "bg-amber-400 text-black",
                      sponsor.sponsor_type === "silver" &&
                        "bg-slate-400 text-black",
                      sponsor.sponsor_type === "bronze" &&
                        "bg-yellow-950 text-white",
                    )}
                  >
                    {sponsor.sponsor_type.charAt(0).toUpperCase() +
                      sponsor.sponsor_type.slice(1)}
                  </span>
                </td>
                <td>
                  <AdminSponsorsActiveCheckbox
                    sponsorId={sponsor.id}
                    initialIsActive={sponsor.is_active}
                  />
                </td>
                <td>
                  <AdminTableActions>
                    <AdminTableEditLink
                      href={reverse("sponsors_edit", {
                        sponsor_id: sponsor.id,
                      })}
                    />
                  </AdminTableActions>
                </td>
              </tr>
            ))}
        </AdminTable>
      </AdminCenteredContentContainer>
    </AdminLayout>
  );
};
