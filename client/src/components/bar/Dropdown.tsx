import { useNavigate } from "react-router-dom";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownSection,
  DropdownItem,
  User,
} from "@nextui-org/react";
import { ThemeSwitcher } from "../ThemeSwitcher";
import { TbLayoutDashboardFilled } from "react-icons/tb";
import { RiFolderUserFill } from "react-icons/ri";
import { IoMdSettings } from "react-icons/io";

export default function DropdownPage() {
  const Navigate = useNavigate();
  const IconClass = "size-5 text-default-500";
  return (
    <Dropdown
      showArrow
      radius="sm"
      classNames={{
        base: "before:bg-default-200", // change arrow background
        content: "p-0 border-small border-divider bg-background",
      }}
    >
      <DropdownTrigger>
        <User
          name="Apollo 11"
          description="@image processing"
          className=" cursor-pointer "
          classNames={{
            name: "text-default-600",
            description: "text-default-500",
          }}
          avatarProps={{
            size: "sm",
            isBordered: true,
            color: "primary",
          }}
        />
      </DropdownTrigger>
      <DropdownMenu
        aria-label="Custom item styles"
        disabledKeys={["profile"]}
        className="p-3"
        itemClasses={{
          base: [
            "rounded-md",
            "text-default-500",
            "transition-opacity",
            "data-[hover=true]:text-foreground",
            "data-[hover=true]:bg-default-100",
            "dark:data-[hover=true]:bg-default-50",
            "data-[selectable=true]:focus:bg-default-50",
            "data-[pressed=true]:opacity-70",
            "data-[focus-visible=true]:ring-default-500",
          ],
        }}
        onAction={(key) => Navigate(String(key))}
      >
        <DropdownSection aria-label="Profile & Actions" showDivider>
          <DropdownItem
            isReadOnly
            key="profile"
            className="opacity-100"
            textValue="Profile"
          >
            <User
              name="Apollo 11"
              description="@image processing"
              classNames={{
                name: "text-default-600",
                description: "text-default-500",
              }}
              avatarProps={{
                size: "sm",
              }}
            />
          </DropdownItem>
          <DropdownItem
            key="/"
            endContent={<TbLayoutDashboardFilled className={IconClass} />}
            textValue="Home"
          >
            Home
          </DropdownItem>
          <DropdownItem
            key="new"
            endContent={<RiFolderUserFill className={IconClass} />}
            textValue="New User"
          >
            New User
          </DropdownItem>
          <DropdownItem
            key="settings"
            endContent={<IoMdSettings className={IconClass} />}
            textValue="Settings"
          >
            Setting
          </DropdownItem>
        </DropdownSection>

        <DropdownSection aria-label="Preferences" showDivider>
          <DropdownItem
            isReadOnly
            key="theme"
            className="cursor-default"
            endContent={<ThemeSwitcher />}
            textValue="Theme"
          >
            Theme
          </DropdownItem>
        </DropdownSection>

        <DropdownSection aria-label="Help & Feedback">
          <DropdownItem key="help_and_feedback" textValue="Help & Feedback">
            Help & Feedback
          </DropdownItem>
          <DropdownItem key="logout" textValue="Log Out">
            Log Out
          </DropdownItem>
        </DropdownSection>
      </DropdownMenu>
    </Dropdown>
  );
}
