import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  useDisclosure,
} from "@nextui-org/react";
import { Button as ButtonAntd } from "antd";
import { MdOutlineCreateNewFolder } from "react-icons/md";

import NewUser from "./NewUser";

export default function FormModel() {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  return (
    <>
      <ButtonAntd
        onClick={onOpen}
        color="default"
        variant="filled"
        icon={
          <MdOutlineCreateNewFolder className="text-default-500" size={18} />
        }
      >
        New Employess
      </ButtonAntd>
      <Modal
        size="xl"
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        isDismissable={false}
        isKeyboardDismissDisabled={true}
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                New
              </ModalHeader>
              <ModalBody>
                <NewUser onClose={onClose} />
              </ModalBody>
              <ModalFooter></ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}
