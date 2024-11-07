import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Image,
} from "@nextui-org/react";
import DropdownPage from "./Dropdown";
export default function NavbarPage() {
  return (
    <Navbar maxWidth="2xl" isBordered>
      <NavbarBrand className="gap-2">
        <Image className=" size-8" radius="none" src="./favicon.ico" alt="Img Brand" />
        <p className="font-bold text-inherit">ADET</p>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem>
            <DropdownPage/>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
