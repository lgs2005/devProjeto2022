import { styled } from "@mui/material";
import { Children, CSSProperties, PropsWithChildren } from "react";

const SContainer = styled('div')`
    display: grid;
    overflow-x: hidden;
    > div {
        grid-area: 1/1;
        transition: opacity ease 300ms, transform ease 300ms;
    }
`;

export default function SwipeTabsContainer(props: PropsWithChildren<{ currentIndex: number }>) {
    return <SContainer>
        {
            Children.map(props.children, (child, index) => {
                let offset = Math.sign(index - props.currentIndex);
                let style: CSSProperties = offset === 0
                    ? {
                        transform: 'none',
                        pointerEvents: 'inherit',
                        opacity: 1,
                    }
                    : {
                        transform: `translateX(calc(100% * ${offset}))`,
                        pointerEvents: 'none',
                        opacity: 0,
                    };

                return <div
                    key={index}
                    children={child}
                    style={style}
                />
            })
        }
    </SContainer>
}