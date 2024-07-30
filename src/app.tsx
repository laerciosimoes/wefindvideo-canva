import { Button, Rows, Text, MultilineInput, CharacterCountDecorator } from "@canva/app-ui-kit";
import { addNativeElement } from "@canva/design";
import styles from "styles/components.css";

export const App = () => {
    const onClick = () => {
        addNativeElement({
            type: "TEXT",
            children: ["Hello world!"],
        });
    };

    return (
        <div className={styles.scrollContainer}>
            <Rows spacing="2u">
                <Text>
                    Insert the prompt for the video generator here.
                </Text>
                <MultilineInput
                    footer={<CharacterCountDecorator max={500} />}
                    onChange={() => { }}
                    placeholder="Your Prompt Data"
                    value="teste"
                />
                <Button variant="primary" onClick={onClick} stretch>
                    Add Video
                </Button>
            </Rows>
        </div>
    );
};
