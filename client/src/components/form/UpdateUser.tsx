import { useState } from "react";
import {
  Avatar,
  AvatarGroup,
  Button,
  Input,
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Textarea,
  useDisclosure,
} from "@nextui-org/react";
import { UploadOutlined } from "@ant-design/icons";
import type { UploadFile, UploadProps } from "antd";
import { Button as ButtonAntd, Upload } from "antd";
import { FaUserEdit } from "react-icons/fa";

interface UpdateUserProps {
  record: {
    key: number;
    name: string;
    image_name: string[];
    note: string;
  };
}

const UpdateUser: React.FC<UpdateUserProps> = ({ record }) => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const handleChange: UploadProps["onChange"] = (info) => {
    let newFileList = [...info.fileList];
    setFileList(newFileList);
  };

  const props: UploadProps = {
    beforeUpload: (file) => {
      setFileList([...fileList, file]);
      return false;
    },
    onChange: handleChange,
    multiple: true,
  };

  return (
    <>
      <Button
        onPress={onOpen}
        size="sm"
        radius="sm"
        variant="flat"
        endContent={<FaUserEdit size={16} className="text-default-500" />}
      >
        Edit
      </Button>
      <Modal
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        isDismissable={false}
        isKeyboardDismissDisabled={true}
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                Update {record.name}
              </ModalHeader>
              <ModalBody>
                <Input
                  startContent={
                    <p className=" text-default-600 text-xs">Name:</p>
                  }
                  defaultValue={record.name}
                />
                <Textarea
                  label="Note"
                  defaultValue={record.note}
                  disableAnimation
                  disableAutosize
                  classNames={{
                    input: "resize-y min-h-[40px]",
                  }}
                />
                <div className="ml-4">
                  <AvatarGroup isBordered>
                    {record.image_name.map((image: string, index: number) => (
                      <button key={index} onClick={() => alert(image)}>
                        <Avatar
                          src={`http://127.0.0.1:8000/${image}`}
                          key={`${image}-${index}`}
                        />
                      </button>
                    ))}
                  </AvatarGroup>
                </div>
                <Upload {...props} fileList={fileList} listType="picture">
                  <ButtonAntd icon={<UploadOutlined />}>Upload</ButtonAntd>
                </Upload>
              </ModalBody>
              <ModalFooter>
                <Button
                  color="danger"
                  variant="light"
                  onPress={onClose}
                  size="sm"
                  radius="sm"
                >
                  Close
                </Button>
                <Button color="success" onPress={onClose} size="sm" radius="sm">
                  Update
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};

export default UpdateUser;
